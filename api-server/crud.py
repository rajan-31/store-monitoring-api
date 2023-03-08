from sqlalchemy.orm import Session, defer

from .database import models, schemas

from uuid import UUID


def create_report(db: Session, report_id: UUID, status: str):
    db_report_status = models.ReportsStatus(report_id=report_id, status=status)
    db.add(db_report_status)
    db.commit()
    db.refresh(db_report_status)

    return db_report_status

def get_report_status(db: Session, report_id: UUID):
    return db.query(models.ReportsStatus).filter(models.ReportsStatus.report_id == report_id).one_or_none()

def get_report_data(db: Session, report_id: UUID):
    return db.query(models.ReportsData)\
    .with_entities(models.ReportsData.store_id, models.ReportsData.uptime_last_hour, models.ReportsData.uptime_last_day, models.ReportsData.uptime_last_week, models.ReportsData.downtime_last_hour, models.ReportsData.downtime_last_day, models.ReportsData.downtime_last_week)\
    .filter(models.ReportsData.report_id == report_id)\
    .all()