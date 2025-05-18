from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.activity import Activity

class ActivityLearner(SQLModel, table=True):
    activity_id: Optional[int] = Field(default=None, foreign_key="activity.id", primary_key=True)
    learner_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)

    activity: "Activity" = Relationship(back_populates="learners_links")
    learner: "User" = Relationship(back_populates="activities_as_learner")
