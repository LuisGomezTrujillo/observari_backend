from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select

from ..models.material import Material
from ..schemas.material import MaterialCreate, MaterialRead, MaterialUpdate
from ..core.database import get_session

router = APIRouter(prefix="/api/materials", tags=["Materials"])


@router.post("/", response_model=MaterialRead, status_code=status.HTTP_201_CREATED)
def create_material(material: MaterialCreate, session: Session = Depends(get_session)):
    db_material = Material.model_validate(material)
    session.add(db_material)
    session.commit()
    session.refresh(db_material)
    return db_material


@router.get("/", response_model=list[MaterialRead])
def read_materials(session: Session = Depends(get_session)):
    materials = session.exec(select(Material)).all()
    return materials


@router.get("/{material_id}", response_model=MaterialRead)
def read_material(material_id: int, session: Session = Depends(get_session)):
    material = session.get(Material, material_id)
    if not material:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material not found")
    return material


@router.patch("/{material_id}", response_model=MaterialRead)
def update_material(
    material_id: int,
    material_update: MaterialUpdate,
    session: Session = Depends(get_session),
):
    material = session.get(Material, material_id)
    if not material:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material not found")

    material_data = material.model_dump()
    update_data = material_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(material, key, value)

    session.add(material)
    session.commit()
    session.refresh(material)
    return material


@router.delete("/{material_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_material(material_id: int, session: Session = Depends(get_session)):
    material = session.get(Material, material_id)
    if not material:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material not found")

    session.delete(material)
    session.commit()
