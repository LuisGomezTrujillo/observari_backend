from pydantic import BaseModel
from typing import Optional
from ..enums import AreaType


class AreaBase(BaseModel):
    title: str
    area_type: AreaType
    environment_id: int


class AreaCreate(AreaBase):
    pass


class AreaRead(AreaBase):
    id: int

    
class AreaUpdate(BaseModel):
    title: Optional[str] = None
    area_type: Optional[AreaType] = None
    environment_id: Optional[int] = None
