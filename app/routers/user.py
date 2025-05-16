from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from app.core.security import get_password_hash, get_current_active_user
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.core.database import get_session
from app.core.security import get_user_by_email

router = APIRouter(prefix="/api", tags=["users"])

@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
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

@router.get("/users/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Endpoint para obtener los datos del usuario autenticado
    """
    return current_user

@router.get("/users", response_model=List[UserRead])
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

@router.get("/users/{user_id}", response_model=UserRead)
def read_user(
    user_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    """
    Endpoint para obtener un usuario por su ID (requiere autenticación)
    """
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"Usuario con ID {user_id} no encontrado")
    return user

@router.put("/users/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    """
    Endpoint para actualizar un usuario por su ID (requiere autenticación)
    """
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail=f"Usuario con ID {user_id} no encontrado")
    
    # Actualizar campos del usuario
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    """
    Endpoint para eliminar un usuario por su ID (requiere autenticación)
    """
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail=f"Usuario con ID {user_id} no encontrado")
    
    db.delete(db_user)
    db.commit()
    return None
