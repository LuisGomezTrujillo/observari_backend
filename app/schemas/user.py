from datetime import datetime
from pydantic import BaseModel, EmailStr

# Esquema para registro de usuario (entrada)
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Esquema para respuesta de usuario (salida)
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    is_active: bool

# Esquema para login
class UserLogin(BaseModel):
    email: EmailStr
    password: str