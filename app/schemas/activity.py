from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ActivityBase(BaseModel):
    name: str
    description: Optional[str] = None

class ActivityCreate(ActivityBase):
    guide_id: Optional[int] = None
    assistant_id: Optional[int] = None

class ActivityRead(ActivityBase):
    id: int
    created_at: datetime
    guide_id: Optional[int] = None
    assistant_id: Optional[int] = None

class ActivityUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    guide_id: Optional[int] = None
    assistant_id: Optional[int] = None
