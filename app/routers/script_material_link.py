from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from ..core.database import get_session
from app.models.script_material_link import ScriptMaterialLink
from app.schemas.script_material_link import (
    ScriptMaterialLinkCreate,
    ScriptMaterialLinkRead,
    ScriptMaterialLinkDelete,
)

router = APIRouter(prefix="/script-material-links", tags=["ScriptMaterialLink"])

@router.post("/", response_model=ScriptMaterialLinkRead, status_code=status.HTTP_201_CREATED)
def create_link(link: ScriptMaterialLinkCreate, session: Session = Depends(get_session)):
    db_link = ScriptMaterialLink(**link.model_dump())
    session.add(db_link)
    session.commit()
    session.refresh(db_link)
    return ScriptMaterialLinkRead.model_validate(db_link)


@router.get("/", response_model=list[ScriptMaterialLinkRead])
def read_links(session: Session = Depends(get_session)):
    results = session.exec(select(ScriptMaterialLink)).all()
    return [ScriptMaterialLinkRead.model_validate(row) for row in results]


@router.get("/{script_id}/{material_id}", response_model=ScriptMaterialLinkRead)
def read_link(script_id: int, material_id: int, session: Session = Depends(get_session)):
    link = session.get(ScriptMaterialLink, (script_id, material_id))
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")
    return ScriptMaterialLinkRead.model_validate(link)


@router.delete("/{script_id}/{material_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_link(script_id: int, material_id: int, session: Session = Depends(get_session)):
    link = session.get(ScriptMaterialLink, (script_id, material_id))
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")
    session.delete(link)
    session.commit()