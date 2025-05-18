from pydantic import BaseModel

class ActivityLearnerLinkBase(BaseModel):
    activity_id: int
    learner_id: int

class ActivityLearnerLinkCreate(ActivityLearnerLinkBase):
    pass

class ActivityLearnerLinkRead(ActivityLearnerLinkBase):
    pass

class ActivityLearnerLinkUpdate(BaseModel):
    # Las claves primarias dobles normalmente no se actualizan,
    # pero se puede incluir si lo deseas
    activity_id: int
    learner_id: int
