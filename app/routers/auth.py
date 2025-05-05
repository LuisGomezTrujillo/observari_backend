from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
import secrets

from app.core.database import get_session
from app.core.security import (
    authenticate_user, 
    create_access_token, 
    get_current_user,
    get_password_hash,
    get_user_by_email
)
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.user import User
from app.schemas.auth import Token, PasswordResetRequest, PasswordReset

# Alias para mantener compatibilidad con código existente
def send_reset_email(email: str, token: str):
    """
    Alias para mantener compatibilidad con código existente
    """
    from app.core.email import send_password_reset_email
    return send_password_reset_email(email, token)

router = APIRouter(prefix="/api", tags=["authentication"])

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_session)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/forgot-password", status_code=status.HTTP_200_OK)
def forgot_password(request: PasswordResetRequest, db: Session = Depends(get_session)):
    """
    Endpoint para solicitar restablecimiento de contraseña
    """
    from app.core.email import send_password_reset_email
    
    user = get_user_by_email(db, email=request.email)
    if not user:
        # Por seguridad, no indicamos si el usuario existe o no
        return {"message": "Si el usuario existe, se enviará un correo con instrucciones"}
    
    # Generar token de restablecimiento
    reset_token = secrets.token_urlsafe(32)
    # Guardar token y fecha de expiración
    user.reset_token = reset_token
    user.reset_token_expires = datetime.now(timezone.utc) + timedelta(minutes=30)
    db.add(user)
    db.commit()
    
    # Enviar correo con el token
    send_password_reset_email(user.email, reset_token)
    
    return {"message": "Si el usuario existe, se enviará un correo con instrucciones"}

@router.post("/reset-password", status_code=status.HTTP_200_OK)
def reset_password(reset_data: PasswordReset, db: Session = Depends(get_session)):
    """
    Endpoint para restablecer la contraseña usando el token enviado por correo
    """
    # Buscar usuario con el token proporcionado
    user = db.exec(select(User).where(User.reset_token == reset_data.token)).first()
    
    # Verificar si el usuario existe y el token es válido
    if not user or not user.reset_token_expires or user.reset_token_expires < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido o expirado"
        )
    
    # Actualizar la contraseña y eliminar el token
    user.hashed_password = get_password_hash(reset_data.new_password)
    user.reset_token = None
    user.reset_token_expires = None
    db.add(user)
    db.commit()
    
    return {"message": "Contraseña actualizada correctamente"}

@router.get("/verify-token/{token}", status_code=status.HTTP_200_OK)
async def verify_token(token: str, db: Session = Depends(get_session)):
    """
    Endpoint para verificar si un token de restablecimiento es válido
    """
    user = db.exec(select(User).where(User.reset_token == token)).first()
    
    if not user or not user.reset_token_expires or user.reset_token_expires < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido o expirado"
        )
    
    return {"valid": True}

@router.get("/users/me", response_model=dict)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Endpoint para obtener información del usuario autenticado
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at
    }