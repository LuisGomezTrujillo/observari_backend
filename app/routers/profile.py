from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.models.profile import Profile
from app.schemas.profile import ProfileCreate, ProfileRead, ProfileUpdate
from app.core.database import get_session

router = APIRouter(prefix="/profiles", tags=["Profiles"])

@router.post("/", response_model=ProfileRead)
def create_profile(profile: ProfileCreate, session: Session = Depends(get_session)):
    db_profile = Profile.model_validate(profile)
    session.add(db_profile)
    session.commit()
    session.refresh(db_profile)
    return db_profile

@router.get("/", response_model=list[ProfileRead])
def read_profiles(session: Session = Depends(get_session)):
    return session.exec(select(Profile)).all()

@router.get("/{profile_id}", response_model=ProfileRead)
def read_profile(profile_id: int, session: Session = Depends(get_session)):
    profile = session.get(Profile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.patch("/{profile_id}", response_model=ProfileRead)
def update_profile(profile_id: int, profile_update: ProfileUpdate, session: Session = Depends(get_session)):
    profile = session.get(Profile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    for field, value in profile_update.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile

@router.delete("/{profile_id}")
def delete_profile(profile_id: int, session: Session = Depends(get_session)):
    profile = session.get(Profile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    session.delete(profile)
    session.commit()
    return {"ok": True}
