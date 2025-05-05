from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from app.core.security import get_password_hash, get_current_active_user
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.database import get_session
from app.core.security import get_user_by_email

router = APIRouter(prefix="/api", tags=["users"])

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_session)):
    """
    Endpoint para registrar un nuevo usuario
    """
    existing_user = get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="El email ya está en uso")

    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Endpoint para obtener los datos del usuario autenticado
    """
    return current_user

@router.get("/users", response_model=List[UserResponse])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    """
    Endpoint para obtener una lista de usuarios (requiere autenticación)
    """
    users = db.exec(select(User).offset(skip).limit(limit)).all()
    return users