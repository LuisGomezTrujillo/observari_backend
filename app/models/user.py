from datetime import datetime, timezone
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr

from app.models.activity import Activity
from app.models.activity_learner import ActivityLearner

if TYPE_CHECKING:
    from app.models.profile import Profile
    from app.models.users_relationship import UsersRelationship
    from app.models.observation import Observation
    from app.models.report import Report

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(index=True, unique=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = Field(default=True)
    reset_token: Optional[str] = Field(default=None)
    reset_token_expires: Optional[datetime] = Field(default=None)

    profile: Optional["Profile"] = Relationship(back_populates="user")

    outgoing_relationships: List["UsersRelationship"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[UsersRelationship.user_id]", "back_populates": "user"}
    )
    incoming_relationships: List["UsersRelationship"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[UsersRelationship.related_user_id]", "back_populates": "related_user"}
    )

    activities_as_guide: List["Activity"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Activity.guide_id]"},
        back_populates="guide"
    )
    activities_as_assistant: List["Activity"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Activity.assistant_id]"},
        back_populates="assistant"
    )
    activities_as_learner: List["ActivityLearner"] = Relationship(
        back_populates="learner"
    )

    observations: List["Observation"] = Relationship(back_populates="observer")
    sent_reports: List["Report"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Report.report_sender]"},
        back_populates="sender"
    )
    received_reports: List["Report"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Report.report_recipient]"},
        back_populates="recipient"
    )
