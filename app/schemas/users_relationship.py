from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel
from pydantic import field_validator
from enum import Enum

class RelationshipType(str, Enum):
    FRIEND = "friend"
    FAMILY = "family"
    COLLEAGUE = "colleague"
    ACQUAINTANCE = "acquaintance"
    OTHER = "other"

class UsersRelationshipBase(SQLModel):
    user_id: int
    related_user_id: int
    relationship_type: RelationshipType
    description: Optional[str] = None
    
    @field_validator('user_id', 'related_user_id')
    @classmethod
    def validate_not_self_relation(cls, v, info):
        # Check that user is not creating relationship with themselves
        values = info.data
        if 'user_id' in values and 'related_user_id' in values and values['user_id'] == values['related_user_id']:
            raise ValueError("Usuario no puede tener relación consigo mismo")
        return v

class UsersRelationshipCreate(UsersRelationshipBase):
    pass

class UsersRelationshipRead(UsersRelationshipBase):
    id: int
    created_at: datetime
    updated_at: datetime

class UsersRelationshipUpdate(SQLModel):
    relationship_type: Optional[RelationshipType] = None
    description: Optional[str] = None
