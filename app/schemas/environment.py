from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from ..enums import EnvironmentType, EnvironmentStatus


class EnvironmentBase(BaseModel):
    title: str
    environment_type: EnvironmentType
    environment_status: EnvironmentStatus
    location: str
    availability: str
    capacity: int
    description: Optional[str]
    photo_url: Optional[str] = None


class EnvironmentCreate(EnvironmentBase):
    pass

class EnvironmentRead(EnvironmentBase):
    id: int
    created_at: datetime
    updated_at: datetime


class EnvironmentUpdate(BaseModel):
    title: Optional[str] = None
    environment_type: Optional[EnvironmentType] = None
    environment_status: EnvironmentStatus
    location: str
    availability: str
    capacity: int
    description: Optional[str]
    photo_url: Optional[str] = None
