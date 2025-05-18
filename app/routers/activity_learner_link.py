from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.models.activity_learner_link import ActivityLearnerLink
from app.schemas.activity_learner_link import ActivityLearnerLinkCreate, ActivityLearnerLinkRead
from app.core.database import get_session

router = APIRouter(prefix="/activity-learner-links", tags=["ActivityLearnerLink"])

@router.post("/", response_model=ActivityLearnerLinkRead)
def create_link(link: ActivityLearnerLinkCreate, session: Session = Depends(get_session)):
    db_link = ActivityLearnerLink(**link.dict())
    session.add(db_link)
    session.commit()
    return db_link

@router.get("/", response_model=list[ActivityLearnerLinkRead])
def read_links(session: Session = Depends(get_session)):
    return session.exec(select(ActivityLearnerLink)).all()

@router.delete("/")
def delete_link(activity_id: int, learner_id: int, session: Session = Depends(get_session)):
    link = session.get(ActivityLearnerLink, (activity_id, learner_id))
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    session.delete(link)
    session.commit()
    return {"ok": True}
