import datetime
from typing import List
from fastapi import Depends, APIRouter, status
from data_base.database import get_db
from data_base import models
from schemas import calendar as calendar_schema
from crud import calendar as calendar_crud
from sqlalchemy.orm import Session

router = APIRouter(tags=["Calendar"])


@router.post("/calendar/", response_model=calendar_schema.CalendarGet, status_code=status.HTTP_201_CREATED)
def create_calendar(calendar: calendar_schema.CalendarCreate, db: Session = Depends(get_db)):
    return calendar_crud.create(db, calendar)


@router.get("/calendar/{calendar_id}", response_model=calendar_schema.CalendarGet, status_code=status.HTTP_200_OK)
def get_calendar(calendar_id: int, db: Session = Depends(get_db)):
    return calendar_crud.read(db, calendar_id)


@router.get("/calendar/", response_model=List[calendar_schema.CalendarGet], status_code=status.HTTP_200_OK)
def get_all_calendar(db: Session = Depends(get_db)):
    return calendar_crud.read_all(db)


@router.put("/calendar/", status_code=status.HTTP_200_OK)
def delete_calendar(calendar: calendar_schema.CalendarBase, db: Session = Depends(get_db)):
    calendar_crud.delete(db, calendar)


@router.put("/calendar/update/", status_code=status.HTTP_200_OK)
def update_calendar(calendar: calendar_schema.CalendarUpdate, db: Session = Depends(get_db)):
    calendar_crud.update(db, calendar)


# @router.get("/calendar/", response_model=calendar_schema.CalendarGet, status_code=status.HTTP_200_OK)
# def get_date(date: datetime.date, db: Session = Depends(get_db)):
#     return calendar_crud.read_date(db, date)
