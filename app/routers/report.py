from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.report import Report
from app.schemas.report import ReportCreate, ReportRead, ReportUpdate
from app.core.database import get_session

router = APIRouter(prefix="/api/reports", tags=["Reports"])

@router.post("/", response_model=ReportRead)
def create_report(report: ReportCreate, session: Session = Depends(get_session)):
    db_report = Report.model_validate(report)
    session.add(db_report)
    session.commit()
    session.refresh(db_report)
    return db_report

@router.get("/", response_model=list[ReportRead])
def read_reports(session: Session = Depends(get_session)):
    return session.exec(select(Report)).all()

@router.get("/{report_id}", response_model=ReportRead)
def read_report(report_id: int, session: Session = Depends(get_session)):
    report = session.get(Report, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@router.patch("/{report_id}", response_model=ReportRead)
def update_report(report_id: int, report_update: ReportUpdate, session: Session = Depends(get_session)):
    report = session.get(Report, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    for field, value in report_update.model_dump(exclude_unset=True).items():
        setattr(report, field, value)
    session.add(report)
    session.commit()
    session.refresh(report)
    return report

@router.delete("/{report_id}")
def delete_report(report_id: int, session: Session = Depends(get_session)):
    report = session.get(Report, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    session.delete(report)
    session.commit()
    return {"ok": True}
