from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import calendar as calendar_schema


def read(db: Session, id: int, user_id: int):
    query = db.query(models.Calendar).filter_by(id=id, user_id=user_id)
    return query.first()


def create(db: Session, calendar: calendar_schema.CalendarCreate, user_id: int):
    calendar_count = db.query(models.Calendar).filter((((models.Calendar.start_date <= calendar.start_date) &
                                                       (models.Calendar.end_date >= calendar.start_date)) |
                                                      ((models.Calendar.start_date <= calendar.end_date) &
                                                       (models.Calendar.end_date >= calendar.end_date)) |
                                                      ((models.Calendar.start_date >= calendar.start_date) &
                                                       (models.Calendar.start_date <= calendar.end_date))) &
                                                      (models.Calendar.user_id == user_id)).count()
    if calendar_count > 0:
        raise HTTPException(status_code=400, detail="This dates are occupied")
    calendar_db = models.Calendar(**calendar.dict(), user_id=user_id)
    db.add(calendar_db)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return calendar_db


def read_all(db: Session, user_company_id: int):
    query = db.query(models.Calendar).filter(
        models.Calendar.id == db.query(models.Company.admin_id).filter_by(id=user_company_id))
    return query.all()


def delete(db: Session, calendar_id: int, user_id: int):
    db.query(models.Calendar).filter_by(id=calendar_id, user_id=user_id).delete()
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def update(db: Session, calendar_id: int, calendar: calendar_schema.CalendarBase, user_id: int):
    calendar_count = db.query(models.Calendar).filter(((models.Calendar.id != calendar_id) &
                                                      (((models.Calendar.start_date <= calendar.start_date) &
                                                        (models.Calendar.end_date >= calendar.start_date)) |
                                                       ((models.Calendar.start_date <= calendar.end_date) &
                                                        (models.Calendar.end_date >= calendar.end_date)) |
                                                       ((models.Calendar.start_date >= calendar.start_date) &
                                                        (models.Calendar.start_date <= calendar.end_date)))) &
                                                      (models.Calendar.user_id == user_id)).count()

    if calendar_count > 0:
        raise HTTPException(status_code=400, detail="This dates are occupied")
    else:
        db.query(models.Calendar).filter_by(id=calendar_id, user_id=user_id).update({**calendar.dict()})
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
