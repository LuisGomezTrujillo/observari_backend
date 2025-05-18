from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.models.activity_learner import ActivityLearner
from app.schemas.activity_learner import ActivityLearnerCreate, ActivityLearnerRead
from app.core.database import get_session

router = APIRouter(prefix="/api/activity-learner", tags=["ActivityLearner"])

@router.post("/", response_model=ActivityLearnerRead)
def create_link(link: ActivityLearnerCreate, session: Session = Depends(get_session)):
    db_link = ActivityLearner(**link.dict())
    session.add(db_link)
    session.commit()
    return db_link

@router.get("/", response_model=list[ActivityLearnerRead])
def read_links(session: Session = Depends(get_session)):
    return session.exec(select(ActivityLearner)).all()

@router.delete("/")
def delete_link(activity_id: int, learner_id: int, session: Session = Depends(get_session)):
    link = session.get(ActivityLearner, (activity_id, learner_id))
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    session.delete(link)
    session.commit()
    return {"ok": True}
