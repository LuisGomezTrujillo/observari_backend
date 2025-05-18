from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.activity_learner import ActivityLearner

class Activity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    guide_id: Optional[int] = Field(default=None, foreign_key="user.id")
    assistant_id: Optional[int] = Field(default=None, foreign_key="user.id")

    guide: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Activity.guide_id]"}, back_populates="activities_as_guide")
    assistant: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Activity.assistant_id]"}, back_populates="activities_as_assistant")
    
    learners_links: List["ActivityLearner"] = Relationship(back_populates="activity")
