from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import datetime, timezone
from typing import Optional, List

from ..models.script import Script
from ..models.area import Area
from ..schemas.script import ScriptCreate, ScriptRead, ScriptUpdate
from ..core.database import get_session

router = APIRouter(prefix="/api/scripts", tags=["Scripts"])


@router.get("/", response_model=List[ScriptRead])
def get_scripts(
    skip: int = 0, 
    limit: int = 100,
    is_active: Optional[bool] = None,
    area_id: Optional[int] = None,
    session: Session = Depends(get_session)
):
    """Get scripts with optional filtering"""
    query = select(Script)
    
    if is_active is not None:
        query = query.where(Script.is_active == is_active)
    
    if area_id is not None:
        query = query.where(Script.area_id == area_id)
    
    query = query.offset(skip).limit(limit)
    scripts = session.exec(query).all()
    return scripts


@router.get("/{script_id}", response_model=ScriptRead)
def get_script(script_id: int, session: Session = Depends(get_session)):
    """Get a specific script by ID"""
    script = session.get(Script, script_id)
    if not script:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Script with id {script_id} not found"
        )
    return script


@router.post("/", response_model=ScriptRead, status_code=status.HTTP_201_CREATED)
def create_script(script_in: ScriptCreate, session: Session = Depends(get_session)):
    """Create a new script"""
    # Validate that area exists
    area = session.get(Area, script_in.area_id)
    if not area:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Area with id {script_in.area_id} does not exist"
        )
    
    # Create script from validated data
    script_data = script_in.model_dump()
    script = Script(**script_data)
    
    session.add(script)
    session.commit()
    session.refresh(script)
    return script


@router.put("/{script_id}", response_model=ScriptRead)
def update_script(
    script_id: int, 
    script_in: ScriptUpdate, 
    session: Session = Depends(get_session)
):
    """Update an existing script"""
    script = session.get(Script, script_id)
    if not script:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Script with id {script_id} not found"
        )
    
    # Get only the fields that were provided
    update_data = script_in.model_dump(exclude_unset=True)
    
    # Validate area if it's being changed
    if "area_id" in update_data:
        area = session.get(Area, update_data["area_id"])
        if not area:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Area with id {update_data['area_id']} does not exist"
            )
    
    # Update script fields
    for key, value in update_data.items():
        setattr(script, key, value)
    
    # Update timestamp
    script.updated_at = datetime.now(timezone.utc)
    
    session.add(script)
    session.commit()
    session.refresh(script)
    return script


@router.patch("/{script_id}/toggle-active", response_model=ScriptRead)
def toggle_script_active(script_id: int, session: Session = Depends(get_session)):
    """Toggle the is_active status of a script"""
    script = session.get(Script, script_id)
    if not script:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Script with id {script_id} not found"
        )
    
    script.is_active = not script.is_active
    script.updated_at = datetime.now(timezone.utc)
    
    session.add(script)
    session.commit()
    session.refresh(script)
    return script


@router.delete("/{script_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_script(script_id: int, session: Session = Depends(get_session)):
    """Delete a script"""
    script = session.get(Script, script_id)
    if not script:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Script with id {script_id} not found"
        )
    
    session.delete(script)
    session.commit()