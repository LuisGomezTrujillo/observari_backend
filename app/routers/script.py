from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from ..models.script import Script
from ..schemas.script import ScriptCreate, ScriptRead
from ..core.database import get_session

router = APIRouter(prefix="/api/scripts", tags=["Scripts"])

@router.get("/", response_model=list[ScriptRead])
def read_scripts(session: Session = Depends(get_session)):
    scripts = session.exec(select(Script)).all()
    return [ScriptRead.model_validate(script) for script in scripts]

@router.get("/{script_id}", response_model=ScriptRead)
def read_script(script_id: int, session: Session = Depends(get_session)):
    script = session.get(Script, script_id)
    if not script:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Script not found")
    return ScriptRead.model_validate(script)

@router.post("/", response_model=ScriptRead, status_code=status.HTTP_201_CREATED)
def create_script(script_in: ScriptCreate, session: Session = Depends(get_session)):
    script = Script(**script_in.model_dump())
    session.add(script)
    session.commit()
    session.refresh(script)
    return ScriptRead.model_validate(script)

@router.put("/{script_id}", response_model=ScriptRead)
def update_script(script_id: int, script_in: ScriptCreate, session: Session = Depends(get_session)):
    script = session.get(Script, script_id)
    if not script:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Script not found")
    for key, value in script_in.model_dump().items():
        setattr(script, key, value)
    session.add(script)
    session.commit()
    session.refresh(script)
    return ScriptRead.model_validate(script)

@router.delete("/{script_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_script(script_id: int, session: Session = Depends(get_session)):
    script = session.get(Script, script_id)
    if not script:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Script not found")
    session.delete(script)
    session.commit()
    return None
