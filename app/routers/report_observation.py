from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.report_observation import ReportObservation
from app.schemas.report_observation import ReportObservationCreate, ReportObservationRead
from app.core.database import get_session

router = APIRouter(prefix="/api/report-observation", tags=["ReportObservation"])

@router.post("/", response_model=ReportObservationRead)
def create_link(link: ReportObservationCreate, session: Session = Depends(get_session)):
    db_link = ReportObservation.model_validate(link)
    session.add(db_link)
    session.commit()
    session.refresh(db_link)
    return db_link

@router.get("/", response_model=list[ReportObservationRead])
def read_links(session: Session = Depends(get_session)):
    return session.exec(select(ReportObservation)).all()

@router.get("/{report_id}/{observation_id}", response_model=ReportObservationRead)
def read_link(report_id: int, observation_id: int, session: Session = Depends(get_session)):
    statement = select(ReportObservation).where(
        ReportObservation.report_id == report_id,
        ReportObservation.observation_id == observation_id
    )
    link = session.exec(statement).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link

@router.delete("/{report_id}/{observation_id}")
def delete_link(report_id: int, observation_id: int, session: Session = Depends(get_session)):
    statement = select(ReportObservation).where(
        ReportObservation.report_id == report_id,
        ReportObservation.observation_id == observation_id
    )
    link = session.exec(statement).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    session.delete(link)
    session.commit()
    return {"ok": True}
