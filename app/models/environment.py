from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel
from ..enums import EnvironmentType, EnvironmentStatus

if TYPE_CHECKING:
    from .area import Area
    from .activity import Activity

class Environment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    environment_type: EnvironmentType = Field(nullable=False)
    environment_status: EnvironmentStatus = Field(nullable=False)
    location: Optional[str]
    availability: str = Field(nullable=False)
    capacity: int = Field(nullable=False)
    description: Optional[str] = None
    photo_url: Optional[str] = None

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    areas: List["Area"] = Relationship(back_populates="environment")
    activities: List["Activity"] = Relationship(back_populates="environment")
