from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import calendar as calendar_schema

def read(db: Session, id: int):
    query = db.query(models.Calendar).filter(models.Calendar.id == id)
    return query.first()

def create(db: Session, calendar: calendar_schema.CalendarCreate):
    calendar_db = models.Calendar(**calendar.dict())
    db.add(calendar_db)
    try:
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e.orig))

def read_all(db: Session):
    query = db.query(models.Calendar)
    return query.all()
