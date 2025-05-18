from pydantic import BaseModel

class ActivityLearnerBase(BaseModel):
    activity_id: int
    learner_id: int

class ActivityLearnerCreate(ActivityLearnerBase):
    pass

class ActivityLearnerRead(ActivityLearnerBase):
    pass

class ActivityLearnerUpdate(BaseModel):
    # Las claves primarias dobles normalmente no se actualizan,
    # pero se puede incluir si lo deseas
    activity_id: int
    learner_id: int
