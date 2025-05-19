from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user import User
    from .report_observation import ReportObservation

class Report(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    report_sender: int = Field(foreign_key="user.id")
    report_recipient: int = Field(foreign_key="user.id")

    report_started: datetime
    report_end: datetime

    sender: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Report.report_sender]"}, back_populates="sent_reports")
    recipient: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Report.report_recipient]"}, back_populates="received_reports")
    observations: List["ReportObservation"] = Relationship(back_populates="report")
