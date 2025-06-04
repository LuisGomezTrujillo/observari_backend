# /schemas/activity_schema.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from ..enums import ActivityType, LessonType


class ActivityBase(BaseModel):
    title: str
    activity_type: ActivityType
    lesson_type: LessonType
    environment_id: int
    area_id: int
    material_id: int
    script_id: int
    guide_id: Optional[int] = None
    assistant_id: Optional[int] = None
    description: Optional[str] = None


class ActivityCreate(ActivityBase):
    pass


class ActivityRead(ActivityBase):
    id: int
    created_at: datetime


class ActivityUpdate(BaseModel):
    title: Optional[str] = None
    activity_type: Optional[ActivityType] = None
    lesson_type: Optional[LessonType] = None
    environment_id: Optional[int] = None
    area_id: Optional[int] = None
    material_id: Optional[int] = None
    script_id: Optional[int] = None
    guide_id: Optional[int] = None
    assistant_id: Optional[int] = None
    description: Optional[str] = None
