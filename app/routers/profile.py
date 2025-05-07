from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.profile import Profile
from app.schemas.profile import ProfileCreate, ProfileRead, ProfileUpdate

router = APIRouter(prefix="/api", tags=["profiles"])

@router.post("/", response_model=ProfileRead)
def create_profile(profile: ProfileCreate, session: Session = Depends(get_session)):
    new_profile = Profile(**profile.model_dump())
    session.add(new_profile)
    session.commit()
    session.refresh(new_profile)
    return new_profile


@router.get("/", response_model=list[ProfileRead])
def read_profiles(session: Session = Depends(get_session)):
    return session.exec(select(Profile)).all()


@router.get("/{profile_id}", response_model=ProfileRead)
def read_profile(profile_id: int, session: Session = Depends(get_session)):
    profile = session.get(Profile, profile_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile


@router.get("/by_user/{user_id}", response_model=ProfileRead)
def get_profile_by_user(user_id: int, session: Session = Depends(get_session)):
    statement = select(Profile).where(Profile.user_id == user_id)
    profile = session.exec(statement).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_201_CREATED, detail="Profile for this user not found")
    return profile


@router.patch("/{profile_id}", response_model=ProfileRead)
def update_profile(profile_id: int, update: ProfileUpdate, session: Session = Depends(get_session)):
    profile = session.get(Profile, profile_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Profile not found")
    for key, value in update.model_dump(exclude_unset=True).items():
        setattr(profile, key, value)
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


@router.delete("/{profile_id}")
def delete_profile(profile_id: int, session: Session = Depends(get_session)):
    profile = session.get(Profile, profile_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    session.delete(profile)
    session.commit()
    return {"ok": True}
