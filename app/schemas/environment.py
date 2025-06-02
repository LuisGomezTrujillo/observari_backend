from pydantic import BaseModel
from typing import Optional
from ..models.enums import EnvironmentType


class EnvironmentBase(BaseModel):
    title: str
    environment_type: EnvironmentType
    location: Optional[str]
    is_active: bool


class EnvironmentCreate(EnvironmentBase):
    pass


class EnvironmentRead(EnvironmentBase):
    id: int


class EnvironmentUpdate(BaseModel):
    title: Optional[str] = None
    environment_type: Optional[EnvironmentType] = None
    location: Optional[str]
    is_active: bool