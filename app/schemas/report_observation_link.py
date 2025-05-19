from pydantic import BaseModel

class ReportObservationLinkBase(BaseModel):
    report_id: int
    observation_id: int

class ReportObservationLinkCreate(ReportObservationLinkBase):
    pass

class ReportObservationLinkRead(ReportObservationLinkBase):
    pass