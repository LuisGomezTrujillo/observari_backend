from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from ..models.script_material_link import ScriptMaterialLink
from ..models.script import Script
from ..models.material import Material
from ..schemas.script_material_link import (
    ScriptMaterialLinkCreate,
    ScriptMaterialLinkRead,
    ScriptMaterialLinkUpdate
)
from ..core.database import get_session

router = APIRouter(prefix="/api/script-material-links", tags=["Script Material Links"])


@router.get("/", response_model=List[ScriptMaterialLinkRead])
def get_script_material_links(session: Session = Depends(get_session)):
    """Get all script-material links"""
    links = session.exec(select(ScriptMaterialLink)).all()
    return links


@router.get("/script/{script_id}", response_model=List[ScriptMaterialLinkRead])
def get_links_by_script(script_id: int, session: Session = Depends(get_session)):
    """Get all material links for a specific script"""
    script = session.get(Script, script_id)
    if not script:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Script with id {script_id} not found"
        )
    
    links = session.exec(
        select(ScriptMaterialLink).where(ScriptMaterialLink.script_id == script_id)
    ).all()
    return links


@router.get("/material/{material_id}", response_model=List[ScriptMaterialLinkRead])
def get_links_by_material(material_id: int, session: Session = Depends(get_session)):
    """Get all script links for a specific material"""
    material = session.get(Material, material_id)
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Material with id {material_id} not found"
        )
    
    links = session.exec(
        select(ScriptMaterialLink).where(ScriptMaterialLink.material_id == material_id)
    ).all()
    return links


@router.get("/{script_id}/{material_id}", response_model=ScriptMaterialLinkRead)
def get_script_material_link(
    script_id: int, 
    material_id: int, 
    session: Session = Depends(get_session)
):
    """Get a specific script-material link"""
    link = session.get(ScriptMaterialLink, (script_id, material_id))
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Link between script {script_id} and material {material_id} not found"
        )
    return link


@router.post("/", response_model=ScriptMaterialLinkRead, status_code=status.HTTP_201_CREATED)
def create_script_material_link(
    link_in: ScriptMaterialLinkCreate, 
    session: Session = Depends(get_session)
):
    """Create a new script-material link"""
    # Validate that script exists
    script = session.get(Script, link_in.script_id)
    if not script:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Script with id {link_in.script_id} not found"
        )
    
    # Validate that material exists
    material = session.get(Material, link_in.material_id)
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Material with id {link_in.material_id} not found"
        )
    
    # Check if link already exists
    existing_link = session.get(ScriptMaterialLink, (link_in.script_id, link_in.material_id))
    if existing_link:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Link between script {link_in.script_id} and material {link_in.material_id} already exists"
        )
    
    # Create the link
    link_data = link_in.model_dump()
    link = ScriptMaterialLink(**link_data)
    
    session.add(link)
    session.commit()
    session.refresh(link)
    return link


@router.put("/{script_id}/{material_id}", response_model=ScriptMaterialLinkRead)
def update_script_material_link(
    script_id: int,
    material_id: int,
    link_in: ScriptMaterialLinkUpdate,
    session: Session = Depends(get_session)
):
    """Update a script-material link"""
    link = session.get(ScriptMaterialLink, (script_id, material_id))
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Link between script {script_id} and material {material_id} not found"
        )
    
    # Get only the fields that were provided
    update_data = link_in.model_dump(exclude_unset=True)
    
    # Update link fields
    for key, value in update_data.items():
        setattr(link, key, value)
    
    session.add(link)
    session.commit()
    session.refresh(link)
    return link


@router.delete("/{script_id}/{material_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_script_material_link(
    script_id: int, 
    material_id: int, 
    session: Session = Depends(get_session)
):
    """Delete a script-material link"""
    link = session.get(ScriptMaterialLink, (script_id, material_id))
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Link between script {script_id} and material {material_id} not found"
        )
    
    session.delete(link)
    session.commit()