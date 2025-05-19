from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ObservationBase(BaseModel):
    observer_id: int
    activity_id: int
    start_time: datetime
    end_time: datetime
    observer_mood: str
    weather_status: str
    objective_description: str
    conclusion: str
    interpretation: str
    time_felt: str
    feelings: str

class ObservationCreate(ObservationBase):
    pass

class ObservationRead(ObservationBase):
    id: int

class ObservationUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    observer_mood: Optional[str] = None
    weather_status: Optional[str] = None
    objective_description: Optional[str] = None
    conclusion: Optional[str] = None
    interpretation: Optional[str] = None
    time_felt: Optional[str] = None
    feelings: Optional[str] = None