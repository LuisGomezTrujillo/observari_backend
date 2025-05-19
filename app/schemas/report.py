from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ReportBase(BaseModel):
    report_sender: int
    report_recipient: int
    report_started: datetime
    report_end: datetime

class ReportCreate(ReportBase):
    pass

class ReportRead(ReportBase):
    id: int

class ReportUpdate(BaseModel):
    report_recipient: Optional[int] = None
    report_started: Optional[datetime] = None
    report_end: Optional[datetime] = None
