from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from ..models.area import Area
from ..schemas.area import AreaCreate, AreaRead, AreaUpdate
from ..core.database import get_session

router = APIRouter(prefix="/api/areas", tags=["Areas"])


@router.post("/", response_model=AreaRead, status_code=status.HTTP_201_CREATED)
def create_area(area_create: AreaCreate, session: Session = Depends(get_session)):
    area = Area.model_validate(area_create)
    session.add(area)
    session.commit()
    session.refresh(area)
    return area


@router.get("/", response_model=list[AreaRead])
def read_areas(session: Session = Depends(get_session)):
    areas = session.exec(select(Area)).all()
    return areas


@router.get("/{area_id}", response_model=AreaRead)
def read_area(area_id: int, session: Session = Depends(get_session)):
    area = session.get(Area, area_id)
    if not area:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Area not found")
    return area


@router.patch("/{area_id}", response_model=AreaRead)
def update_area(area_id: int, area_update: AreaUpdate, session: Session = Depends(get_session)):
    area = session.get(Area, area_id)
    if not area:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Area not found")
    
    area_data = area.model_dump()
    update_data = area_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(area, key, value)

    session.add(area)
    session.commit()
    session.refresh(area)
    return area


@router.delete("/{area_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_area(area_id: int, session: Session = Depends(get_session)):
    area = session.get(Area, area_id)
    if not area:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Area not found")
    session.delete(area)
    session.commit()
