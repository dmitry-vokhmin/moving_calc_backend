import datetime
from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import calendar as calendar_schema


def read(db: Session, id: int):
    query = db.query(models.Calendar).filter(models.Calendar.id == id)
    return query.first()


def create(db: Session, calendar: calendar_schema.CalendarCreate):
    calendar_count = db.query(models.Calendar).filter(((models.Calendar.start_date <= calendar.start_date) &
                                                       (models.Calendar.end_date >= calendar.start_date)) |
                                                      ((models.Calendar.start_date <= calendar.end_date) &
                                                       (models.Calendar.end_date >= calendar.end_date)) |
                                                      ((models.Calendar.start_date >= calendar.start_date) &
                                                       (models.Calendar.start_date <= calendar.end_date))).count()
    if calendar_count > 0:
        raise HTTPException(status_code=400, detail="This dates are occupied")
    calendar_db = models.Calendar(**calendar.dict())
    db.add(calendar_db)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e.orig))
    return calendar_db


def read_date(db: Session, date: datetime.date):
    calendar_db = db.query(models.Calendar).filter(models.Calendar.start_date <= date,
                                                   models.Calendar.end_date >= date)
    return calendar_db.first()


def read_all(db: Session):
    query = db.query(models.Calendar)
    return query.all()


def delete(db: Session, calendar: calendar_schema.CalendarBase):
    db.query(models.Calendar).filter((models.Calendar.start_date == calendar.start_date) &
                                     (models.Calendar.end_date == calendar.end_date)).delete()
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e.orig))


def update(db: Session, calendar: calendar_schema.CalendarUpdate):
    #TODO: Написать логику update
    pass
