from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.users_relationship import RelationshipType

class UsersRelationshipBase(BaseModel):
    user_id: int
    related_user_id: int
    relationship_type: RelationshipType
    description: Optional[str] = None

class UsersRelationshipCreate(UsersRelationshipBase):
    pass

class UsersRelationshipRead(UsersRelationshipBase):
    id: int
    created_at: datetime
    updated_at: datetime

class UsersRelationshipUpdate(BaseModel):
    relationship_type: Optional[RelationshipType] = None
    description: Optional[str] = None
