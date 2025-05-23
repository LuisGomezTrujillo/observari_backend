from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.models.report_observation_link import ReportObservationLink
from app.schemas.report_observation_link import ReportObservationLinkCreate, ReportObservationLinkRead
from app.core.database import get_session

router = APIRouter(prefix="/api/report-observation-links", tags=["ReportObservationLinks"])

@router.post("/", response_model=ReportObservationLinkRead, status_code=status.HTTP_201_CREATED)
def create_link(link: ReportObservationLinkCreate, session: Session = Depends(get_session)):
    db_link = ReportObservationLink.model_validate(link)
    session.add(db_link)
    session.commit()
    session.refresh(db_link)
    return db_link

@router.get("/", response_model=list[ReportObservationLinkRead])
def read_links(session: Session = Depends(get_session)):
    return session.exec(select(ReportObservationLink)).all()

@router.get("/{report_id}/{observation_id}", response_model=ReportObservationLinkRead)
def read_link(report_id: int, observation_id: int, session: Session = Depends(get_session)):
    statement = select(ReportObservationLink).where(
        ReportObservationLink.report_id == report_id,
        ReportObservationLink.observation_id == observation_id
    )
    link = session.exec(statement).first()
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")
    return link

@router.delete("/{report_id}/{observation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_link(report_id: int, observation_id: int, session: Session = Depends(get_session)):
    statement = select(ReportObservationLink).where(
        ReportObservationLink.report_id == report_id,
        ReportObservationLink.observation_id == observation_id
    )
    link = session.exec(statement).first()
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")
    session.delete(link)
    session.commit()
    return {"ok": True}
