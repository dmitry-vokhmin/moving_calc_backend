import datetime as dt
from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import calendar as calendar_schema
from security.security import get_user, check_privilege


def check_date_order(calendar):
    start_date = calendar.start_date
    end_date = calendar.end_date
    if end_date < start_date:
        calendar.start_date = end_date
        calendar.end_date = start_date
    return calendar


def create(db: Session, calendar: calendar_schema.CalendarCreate, user_company_id: int):
    calendar_count = db.query(models.Calendar).filter((((models.Calendar.start_date <= calendar.start_date) &
                                                        (models.Calendar.end_date >= calendar.start_date)) |
                                                       ((models.Calendar.start_date <= calendar.end_date) &
                                                        (models.Calendar.end_date >= calendar.end_date)) |
                                                       ((models.Calendar.start_date >= calendar.start_date) &
                                                        (models.Calendar.start_date <= calendar.end_date))) &
                                                      (models.Calendar.company_id == user_company_id)).count()
    if calendar_count > 0:
        raise HTTPException(status_code=400, detail="This dates are occupied")
    calendar_db = models.Calendar(**calendar.dict(), company_id=user_company_id)
    db.add(calendar_db)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return calendar_db


def read_all(db: Session, user_id: int):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        query = db.query(models.Calendar)
    else:
        query = db.query(models.Calendar).filter_by(company_id=user_db.company_id)
    return query.all()


def update(db: Session, calendar: calendar_schema.CalendarCreate, user_id: int):
    calendar = check_date_order(calendar)
    user_db = get_user(db, user_id)
    check_privilege(db, user_db, "configurations")
    try:
        create(db, calendar, user_db.company_id)
    except HTTPException:
        separate_dates(db, calendar, user_db, user_id)
        delete_middle_date(db, calendar, user_db)
        update_end_date(db, calendar, user_db)
        update_start_date(db, calendar, user_db)
        create(db, calendar, user_db.company_id)


def separate_dates(db, calendar, user_db, user_id):
    dates = db.query(models.Calendar).filter(((models.Calendar.start_date < calendar.start_date) &
                                              (models.Calendar.end_date > calendar.end_date)) &
                                             (models.Calendar.company_id == user_db.company_id)).first()
    if dates:
        new_end_date = dates.end_date
        new_price_tag_id = dates.price_tag_id
        db.query(models.Calendar).filter_by(id=dates.id).update(
            {"end_date": calendar.start_date - dt.timedelta(days=1)})
        new_model = calendar_schema.CalendarCreate(
            start_date=calendar.start_date + dt.timedelta(days=1),
            end_date=new_end_date,
            price_tag_id=new_price_tag_id
        )
        create(db, new_model, user_id)


def delete_middle_date(db, calendar, user_db):
    db.query(models.Calendar).filter(((models.Calendar.start_date >= calendar.start_date) &
                                      (models.Calendar.end_date <= calendar.end_date)) &
                                     (models.Calendar.company_id == user_db.company_id)).delete()


def update_end_date(db, calendar, user_db):
    db.query(models.Calendar).filter(((models.Calendar.start_date < calendar.start_date) &
                                      (models.Calendar.end_date >= calendar.start_date)) &
                                     (models.Calendar.company_id == user_db.company_id)).update(
        {"end_date": calendar.start_date - dt.timedelta(days=1)})


def update_start_date(db, calendar, user_db):
    db.query(models.Calendar).filter(((models.Calendar.start_date <= calendar.end_date) &
                                      (models.Calendar.end_date > calendar.end_date)) &
                                     (models.Calendar.company_id == user_db.company_id)).update(
        {"start_date": calendar.end_date + dt.timedelta(days=1)})
