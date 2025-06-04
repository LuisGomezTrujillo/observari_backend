from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from ..enums import ActivityType, LessonType

if TYPE_CHECKING:
    from .user import User
    from .activity_learner import ActivityLearner
    from .environment import Environment
    from .area import Area
    from .material import Material
    from .script import Script

class Activity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)    
    title: str
    activity_type: ActivityType
    lesson_type: LessonType
    environment_id: int = Field(foreign_key="environment.id")
    area_id: int = Field(foreign_key="area.id")
    material_id: int = Field(foreign_key="material.id")
    script_id: int = Field(foreign_key="script.id")
        
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    guide_id: Optional[int] = Field(default=None, foreign_key="user.id")
    assistant_id: Optional[int] = Field(default=None, foreign_key="user.id")

    environment: Optional["Environment"] = Relationship(back_populates="activities")
    area: Optional["Area"] = Relationship(back_populates="activities")
    material: Optional["Material"] = Relationship(back_populates="activities")
    script: Optional["Script"] = Relationship(back_populates="activities")

    guide: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Activity.guide_id]"}, back_populates="activities_as_guide")
    assistant: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Activity.assistant_id]"}, back_populates="activities_as_assistant")
    
    learners_links: List["ActivityLearner"] = Relationship(back_populates="activity")
