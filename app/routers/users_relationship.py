from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.models.users_relationship import UsersRelationship
from app.schemas.users_relationship import UsersRelationshipCreate, UsersRelationshipRead, UsersRelationshipUpdate
from app.core.database import get_session

router = APIRouter(prefix="/api/relationships", tags=["UsersRelationships"])

@router.post("/", response_model=UsersRelationshipRead, status_code=status.HTTP_201_CREATED)
def create_relationship(data: UsersRelationshipCreate, session: Session = Depends(get_session)):
    db_obj = UsersRelationship.model_validate(data)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

@router.get("/", response_model=list[UsersRelationshipRead])
def read_relationships(session: Session = Depends(get_session)):
    return session.exec(select(UsersRelationship)).all()

@router.get("/{relationship_id}", response_model=UsersRelationshipRead)
def read_relationship(relationship_id: int, session: Session = Depends(get_session)):
    relationship = session.get(UsersRelationship, relationship_id)
    if not relationship:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relationship not found")
    return relationship

@router.patch("/{relationship_id}", response_model=UsersRelationshipRead)
def update_relationship(relationship_id: int, data: UsersRelationshipUpdate, session: Session = Depends(get_session)):
    relationship = session.get(UsersRelationship, relationship_id)
    if not relationship:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relationship not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(relationship, field, value)
    session.add(relationship)
    session.commit()
    session.refresh(relationship)
    return relationship

@router.delete("/{relationship_id}")
def delete_relationship(relationship_id: int, session: Session = Depends(get_session)):
    relationship = session.get(UsersRelationship, relationship_id)
    if not relationship:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Relationship not found")
    session.delete(relationship)
    session.commit()
    return {"ok": True}
