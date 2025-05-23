# /routers/activity_router.py
from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from ..models.activity import Activity
from ..schemas.activity import ActivityCreate, ActivityRead, ActivityUpdate

router = APIRouter(prefix="/api/activities", tags=["Activities"])


def get_session():
    from ..core.database import get_session  # define your SessionLocal

@router.get("/", response_model=list[ActivityRead], status_code=status.HTTP_201_CREATED)
def read_activities(session: Session = Depends(get_session)):
    activities = session.exec(select(Activity)).all()
    return [ActivityRead.model_validate(act) for act in activities]


@router.get("/{activity_id}", response_model=ActivityRead)
def read_activity(activity_id: int, session: Session = Depends(get_session)):
    activity = session.get(Activity, activity_id)
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
    return ActivityRead.model_validate(activity)


@router.post("/", response_model=ActivityRead, status_code=status.HTTP_201_CREATED)
def create_activity(activity: ActivityCreate, session: Session = Depends(get_session)):
    db_activity = Activity(**activity.model_dump())
    session.add(db_activity)
    session.commit()
    session.refresh(db_activity)
    return ActivityRead.model_validate(db_activity)


@router.put("/{activity_id}", response_model=ActivityRead)
def update_activity(activity_id: int, activity_data: ActivityUpdate, session: Session = Depends(get_session)):
    db_activity = session.get(Activity, activity_id)
    if not db_activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")

    for key, value in activity_data.model_dump(exclude_unset=True).items():
        setattr(db_activity, key, value)

    session.add(db_activity)
    session.commit()
    session.refresh(db_activity)
    return ActivityRead.model_validate(db_activity)


@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_activity(activity_id: int, session: Session = Depends(get_session)):
    db_activity = session.get(Activity, activity_id)
    if not db_activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")

    session.delete(db_activity)
    session.commit()
