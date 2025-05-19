from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .report import Report
    from .observation import Observation

class ReportObservationLink(SQLModel, table=True):
    report_id: Optional[int] = Field(default=None, foreign_key="report.id", primary_key=True)
    observation_id: Optional[int] = Field(default=None, foreign_key="observation.id", primary_key=True)

    report: Optional["Report"] = Relationship(back_populates="observations")
    observation: Optional["Observation"] = Relationship(back_populates="reports")