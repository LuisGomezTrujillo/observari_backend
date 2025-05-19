from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user import User
    from .activity import Activity
    from .report_observation_link import ReportObservationLink

class Observation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    observer_id: int = Field(foreign_key="user.id")
    activity_id: int = Field(foreign_key="activity.id")

    start_time: datetime
    end_time: datetime
    observer_mood: str
    weather_status: str
    objective_description: str
    conclusion: str
    interpretation: str
    time_felt: str
    feelings: str

    observer: Optional["User"] = Relationship(back_populates="observations")
    activity: Optional["Activity"] = Relationship()
    reports: List["ReportObservationLink"] = Relationship(back_populates="observation")