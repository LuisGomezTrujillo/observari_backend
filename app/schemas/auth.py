from typing import Optional
from pydantic import BaseModel, EmailStr

# Esquema para token de acceso
class Token(BaseModel):
    access_token: str
    token_type: str

# Esquema para datos dentro del token
class TokenData(BaseModel):
    username: Optional[str] = None

# Esquema para solicitud de restablecimiento de contraseña
class PasswordResetRequest(BaseModel):
    email: EmailStr

# Esquema para cambio de contraseña
class PasswordReset(BaseModel):
    token: str
    new_password: str