from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..core.database import get_session
from ..models.activity_learner import ActivityLearner
from ..schemas.activity_learner import (
    ActivityLearnerCreate,
    ActivityLearnerRead,
    ActivityLearnerDelete
)

router = APIRouter(prefix="/api/activity-learner", tags=["ActivityLearner"])

@router.post("/", response_model=ActivityLearnerRead, status_code=status.HTTP_201_CREATED)
def create_activity_learner(
    data: ActivityLearnerCreate, session: Session = Depends(get_session)
):
    link = ActivityLearner.model_validate(data)
    session.add(link)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This learner is already linked to the activity.",
        )
    session.refresh(link)
    return link

@router.get("/", response_model=list[ActivityLearnerRead])
def get_all_links(session: Session = Depends(get_session)):
    links = session.exec(select(ActivityLearner)).all()
    return [ActivityLearnerRead.model_validate(link) for link in links]

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_activity_learner(
    data: ActivityLearnerDelete, session: Session = Depends(get_session)
):
    link = session.get(ActivityLearner, (data.activity_id, data.learner_id))
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link not found."
        )
    session.delete(link)
    session.commit()
