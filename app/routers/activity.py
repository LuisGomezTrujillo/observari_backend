from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.models.activity import Activity
from app.schemas.activity import ActivityCreate, ActivityRead, ActivityUpdate
from app.core.database import get_session

router = APIRouter(prefix="/api/activities", tags=["Activities"])

@router.post("/", response_model=ActivityRead)
def create_activity(activity: ActivityCreate, session: Session = Depends(get_session)):
    db_activity = Activity.model_validate(activity)
    session.add(db_activity)
    session.commit()
    session.refresh(db_activity)
    return db_activity

@router.get("/", response_model=list[ActivityRead])
def read_activities(session: Session = Depends(get_session)):
    return session.exec(select(Activity)).all()

@router.get("/{activity_id}", response_model=ActivityRead)
def read_activity(activity_id: int, session: Session = Depends(get_session)):
    activity = session.get(Activity, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity

@router.patch("/{activity_id}", response_model=ActivityRead)
def update_activity(activity_id: int, activity_update: ActivityUpdate, session: Session = Depends(get_session)):
    activity = session.get(Activity, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    for field, value in activity_update.model_dump(exclude_unset=True).items():
        setattr(activity, field, value)
    session.add(activity)
    session.commit()
    session.refresh(activity)
    return activity

@router.delete("/{activity_id}")
def delete_activity(activity_id: int, session: Session = Depends(get_session)):
    activity = session.get(Activity, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    session.delete(activity)
    session.commit()
    return {"ok": True}
