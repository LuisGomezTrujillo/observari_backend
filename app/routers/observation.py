from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.observation import Observation
from app.schemas.observation import ObservationCreate, ObservationRead, ObservationUpdate
from app.core.database import get_session

router = APIRouter(prefix="/api/observations", tags=["Observations"])

@router.post("/", response_model=ObservationRead)
def create_observation(observation: ObservationCreate, session: Session = Depends(get_session)):
    db_observation = Observation.model_validate(observation)
    session.add(db_observation)
    session.commit()
    session.refresh(db_observation)
    return db_observation

@router.get("/", response_model=list[ObservationRead])
def read_observations(session: Session = Depends(get_session)):
    return session.exec(select(Observation)).all()

@router.get("/{observation_id}", response_model=ObservationRead)
def read_observation(observation_id: int, session: Session = Depends(get_session)):
    observation = session.get(Observation, observation_id)
    if not observation:
        raise HTTPException(status_code=404, detail="Observation not found")
    return observation

@router.patch("/{observation_id}", response_model=ObservationRead)
def update_observation(observation_id: int, observation_update: ObservationUpdate, session: Session = Depends(get_session)):
    observation = session.get(Observation, observation_id)
    if not observation:
        raise HTTPException(status_code=404, detail="Observation not found")
    for field, value in observation_update.model_dump(exclude_unset=True).items():
        setattr(observation, field, value)
    session.add(observation)
    session.commit()
    session.refresh(observation)
    return observation

@router.delete("/{observation_id}")
def delete_observation(observation_id: int, session: Session = Depends(get_session)):
    observation = session.get(Observation, observation_id)
    if not observation:
        raise HTTPException(status_code=404, detail="Observation not found")
    session.delete(observation)
    session.commit()
    return {"ok": True}
