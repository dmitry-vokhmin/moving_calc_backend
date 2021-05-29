from typing import List
from fastapi import Depends, APIRouter, status
from data_base.database import get_db
from schemas import calendar as calendar_schema
from crud import calendar as calendar_crud
from sqlalchemy.orm import Session
from security.security import get_current_user

router = APIRouter(tags=["Calendar"])


@router.post("/calendar/", response_model=calendar_schema.CalendarGet, status_code=status.HTTP_201_CREATED)
def create_calendar(calendar: calendar_schema.CalendarCreate,
                    db: Session = Depends(get_db),
                    user_id=Depends(get_current_user)):
    return calendar_crud.create(db, calendar, user_id)


@router.get("/calendar/{calendar_id}", response_model=calendar_schema.CalendarGet, status_code=status.HTTP_200_OK)
def get_calendar(calendar_id: int, db: Session = Depends(get_db), user_id=Depends(get_current_user)):
    return calendar_crud.read(db, calendar_id, user_id)


@router.get("/calendar/", response_model=List[calendar_schema.CalendarGet], status_code=status.HTTP_200_OK)
def get_all_calendar(db: Session = Depends(get_db), user_id=Depends(get_current_user)):
    return calendar_crud.read_all(db, user_id)


@router.put("/calendar/", status_code=status.HTTP_200_OK)
def update_calendar(calendar: calendar_schema.CalendarCreate,
                    db: Session = Depends(get_db),
                    user_id=1):
    calendar_crud.update(db, calendar, user_id)
