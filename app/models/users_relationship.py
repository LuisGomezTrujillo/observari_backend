from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from enum import Enum

if TYPE_CHECKING:
    from app.models.user import User

class RelationshipType(str, Enum):
    FRIEND = "friend"
    FAMILY = "family"
    COLLEAGUE = "colleague"
    ACQUAINTANCE = "acquaintance"
    OTHER = "other"

class UsersRelationship(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    related_user_id: int = Field(foreign_key="user.id", nullable=False)
    relationship_type: RelationshipType = Field(nullable=False)
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationships
    user: "User" = Relationship(sa_relationship_kwargs={"foreign_keys": "[UsersRelationship.user_id]"})
    related_user: "User" = Relationship(sa_relationship_kwargs={"foreign_keys": "[UsersRelationship.related_user_id]"})