from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from ..core.database import get_session
from ..models.environment import Environment
from ..schemas.environment import EnvironmentCreate, EnvironmentRead, EnvironmentUpdate

router = APIRouter(prefix="/api/environments", tags=["Environments"])


@router.post("/", response_model=EnvironmentRead, status_code=status.HTTP_201_CREATED)
def create_environment(environment: EnvironmentCreate, session: Session = Depends(get_session)):
    db_environment = Environment.model_validate(environment)
    session.add(db_environment)
    session.commit()
    session.refresh(db_environment)
    return db_environment


@router.get("/", response_model=List[EnvironmentRead])
def read_environments(session: Session = Depends(get_session)):
    environments = session.exec(select(Environment)).all()
    return environments


@router.get("/{environment_id}", response_model=EnvironmentRead)
def read_environment(environment_id: int, session: Session = Depends(get_session)):
    environment = session.get(Environment, environment_id)
    if not environment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Environment not found")
    return environment


@router.patch("/{environment_id}", response_model=EnvironmentRead)
def update_environment(environment_id: int, environment_update: EnvironmentUpdate, session: Session = Depends(get_session)):
    db_environment = session.get(Environment, environment_id)
    if not db_environment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Environment not found")

    env_data = environment_update.model_dump(exclude_unset=True)
    for key, value in env_data.items():
        setattr(db_environment, key, value)

    session.add(db_environment)
    session.commit()
    session.refresh(db_environment)
    return db_environment


@router.delete("/{environment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_environment(environment_id: int, session: Session = Depends(get_session)):
    environment = session.get(Environment, environment_id)
    if not environment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Environment not found")

    session.delete(environment)
    session.commit()
