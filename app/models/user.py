# Añadir estas líneas al archivo app/models/user.py
from datetime import datetime, timezone
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr

if TYPE_CHECKING:
    from app.models.profile import Profile
    from app.models.users_relationship import UsersRelationship

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(index=True, unique=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = Field(default=True)
    reset_token: Optional[str] = Field(default=None)
    reset_token_expires: Optional[datetime] = Field(default=None)

    profile: Optional["Profile"] = Relationship(back_populates="user")
   
    # Añadir estas relaciones
    outgoing_relationships: List["UsersRelationship"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[UsersRelationship.user_id]", "back_populates": "user"}
    )
    incoming_relationships: List["UsersRelationship"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[UsersRelationship.related_user_id]", "back_populates": "related_user"}
    )
