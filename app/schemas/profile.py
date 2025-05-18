from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel

class ProfileBase(BaseModel):
    first_name: str
    second_name: Optional[str] = None
    last_name: str
    second_last_name: Optional[str] = None
    photo_url: Optional[str] = None
    birth_date: date
    mobile_phone: Optional[str] = None
    home_address: Optional[str] = None
    role: Optional[str] = None

class ProfileCreate(ProfileBase):
    user_id: int

class ProfileRead(ProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

class ProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    second_name: Optional[str] = None
    last_name: Optional[str] = None
    second_last_name: Optional[str] = None
    photo_url: Optional[str] = None
    birth_date: Optional[date] = None
    mobile_phone: Optional[str] = None
    home_address: Optional[str] = None
    role: Optional[str] = None
