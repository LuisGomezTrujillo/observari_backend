from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional, List
from datetime import date, datetime


class ScriptBase(BaseModel):
    title: str
    area_id: int
    age_range: str
    objective: str
    steps: str
    duration_minutes: int
    created_by: str
    uploaded_by: str
    illustrations_url: Optional[str] = None
    video_url: Optional[str] = None
    pdf_url: Optional[str] = None
    reviewed_by: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    is_active: bool = True

    @field_validator("tags", mode="before")
    @classmethod
    def parse_tags(cls, v):
        if isinstance(v, str):
            return [tag.strip() for tag in v.split(",") if tag.strip()]
        elif v is None:
            return None
        return v

    def model_dump(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)
        # Convert tags list back to string for database storage
        if isinstance(data.get("tags"), list):
            data["tags"] = ",".join(data["tags"])
        return data


class ScriptCreate(ScriptBase):
    pass


class ScriptUpdate(BaseModel):
    title: Optional[str] = None
    area_id: Optional[int] = None
    age_range: Optional[str] = None
    objective: Optional[str] = None
    steps: Optional[str] = None
    duration_minutes: Optional[int] = None
    created_by: Optional[str] = None
    uploaded_by: Optional[str] = None
    reviewed_by: Optional[str] = None
    illustrations_url: Optional[str] = None
    video_url: Optional[str] = None
    pdf_url: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None

    @field_validator("tags", mode="before")
    @classmethod
    def parse_tags(cls, v):
        if isinstance(v, str):
            return [tag.strip() for tag in v.split(",") if tag.strip()]
        elif v is None:
            return None
        return v

    def model_dump(self, *args, exclude_unset=False, **kwargs):
        data = super().model_dump(*args, exclude_unset=exclude_unset, **kwargs)
        # Convert tags list back to string for database storage
        if isinstance(data.get("tags"), list):
            data["tags"] = ",".join(data["tags"])
        return data


class ScriptRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    area_id: int
    age_range: str
    objective: str
    steps: str
    duration_minutes: int
    created_by: str
    uploaded_by: str
    illustrations_url: Optional[str] = None
    video_url: Optional[str] = None
    pdf_url: Optional[str] = None
    reviewed_by: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    is_active: bool
    created_at: date
    updated_at: datetime
    uploaded_at: datetime

    @field_validator("tags", mode="before")
    @classmethod
    def parse_tags(cls, v):
        if isinstance(v, str):
            return [tag.strip() for tag in v.split(",") if tag.strip()]
        elif v is None:
            return None
        return v
