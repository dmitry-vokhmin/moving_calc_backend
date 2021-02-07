from typing import List
from fastapi import Depends, APIRouter, status
from data_base.database import get_db
from data_base import models
from schemas import phone_number as phone_number_schema
from crud import phone_number as phone_number_crud
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/phone_number/", status_code=status.HTTP_201_CREATED)
def create_phone_number(phone_number: phone_number_schema.PhoneNumberCreate, db: Session = Depends(get_db)):
    phone_number_crud.create(db, phone_number)


@router.get("/phone_number/{phone_number_id}",
            response_model=phone_number_schema.PhoneNumberGet,
            status_code=status.HTTP_200_OK)
def get_phone_number(phone_number_id: int, db: Session = Depends(get_db)):
    return phone_number_crud.read(db, phone_number_id)


@router.get("/phone_number/", response_model=List[phone_number_schema.PhoneNumberGet], status_code=status.HTTP_200_OK)
def get_all_phone_numbers(db: Session = Depends(get_db)):
    return phone_number_crud.read_all(db)
