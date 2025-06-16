from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from datetime import datetime, timezone
from typing import List, Optional

from ..models.material import Material
from ..schemas.material import MaterialCreate, MaterialRead, MaterialUpdate
from ..core.database import get_session

router = APIRouter(prefix="/api/materials", tags=["Materials"])


@router.get("/", response_model=List[MaterialRead])
def get_materials(
    skip: int = 0,
    limit: int = 100,
    area_id: Optional[int] = None,
    session: Session = Depends(get_session)
):
    """Get materials with optional filtering"""
    query = select(Material)
    
    if area_id is not None:
        query = query.where(Material.area_id == area_id)
    
    query = query.offset(skip).limit(limit)
    materials = session.exec(query).all()
    return materials


@router.get("/{material_id}", response_model=MaterialRead)
def get_material(material_id: int, session: Session = Depends(get_session)):
    """Get a specific material by ID"""
    material = session.get(Material, material_id)
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Material with id {material_id} not found"
        )
    return material


@router.post("/", response_model=MaterialRead, status_code=status.HTTP_201_CREATED)
def create_material(material_in: MaterialCreate, session: Session = Depends(get_session)):
    """Create a new material"""
    material_data = material_in.model_dump()
    material = Material(**material_data)
    
    session.add(material)
    session.commit()
    session.refresh(material)
    return material


@router.put("/{material_id}", response_model=MaterialRead)
def update_material(
    material_id: int,
    material_in: MaterialUpdate,
    session: Session = Depends(get_session),
):
    """Update an existing material"""
    material = session.get(Material, material_id)
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Material with id {material_id} not found"
        )

    # Get only the fields that were provided
    update_data = material_in.model_dump(exclude_unset=True)
    
    # Update material fields
    for key, value in update_data.items():
        setattr(material, key, value)
    
    # Update timestamp
    material.updated_at = datetime.now(timezone.utc)

    session.add(material)
    session.commit()
    session.refresh(material)
    return material


@router.delete("/{material_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_material(material_id: int, session: Session = Depends(get_session)):
    """Delete a material"""
    material = session.get(Material, material_id)
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Material with id {material_id} not found"
        )

    session.delete(material)
    session.commit()