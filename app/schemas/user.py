from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    
    # @field_validator("password")
    # def password_min_length(cls, v):
    #     if len(v) < 8:
    #         raise ValueError("La contraseña debe tener al menos 8 caracteres")
    #     return v

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    # No incluimos password aquí, debería ser un endpoint separado para cambiar contraseñas

class UserResponse(UserBase):
    id: int
    role: str = "Usuario"
    is_active: bool = True
    