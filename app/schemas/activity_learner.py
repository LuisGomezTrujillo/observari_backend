from pydantic import BaseModel

class ActivityLearnerBase(BaseModel):
    activity_id: int
    learner_id: int

class ActivityLearnerCreate(ActivityLearnerBase):
    pass

class ActivityLearnerRead(ActivityLearnerBase):
    pass

class ActivityLearnerDelete(BaseModel):
    activity_id: int
    learner_id: int
