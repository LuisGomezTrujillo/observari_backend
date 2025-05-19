from pydantic import BaseModel

class ReportObservationBase(BaseModel):
    report_id: int
    observation_id: int

class ReportObservationCreate(ReportObservationBase):
    pass

class ReportObservationRead(ReportObservationBase):
    pass