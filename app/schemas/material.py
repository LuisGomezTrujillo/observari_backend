from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from ..enums import MaterialStatus


class MaterialBase(BaseModel):
    title: str
    reference: str
    description: Optional[str] = None
    photo_url: Optional[str] = None
    status: MaterialStatus
    area_id: int


class MaterialCreate(MaterialBase):
    pass


class MaterialRead(MaterialBase):
    id: int
    created_at: datetime
    updated_at: datetime


class MaterialUpdate(BaseModel):
    title: Optional[str] = None
    reference: Optional[str] = None
    description: Optional[str] = None
    photo_url: Optional[str] = None
    status: Optional[MaterialStatus] = None
    area_id: Optional[int] = None
