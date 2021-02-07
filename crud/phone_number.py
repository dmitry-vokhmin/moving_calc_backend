from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import phone_number as phone_number_schema


def read(db: Session, id: int):
    query = db.query(models.PhoneNumber).filter(models.PhoneNumber.id == id)
    return query.first()


def create(db: Session, phone_number: phone_number_schema.PhoneNumberCreate):
    phone_number_db = models.PhoneNumber(**phone_number.dict())
    db.add(phone_number_db)
    try:
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e.orig))


def read_all(db: Session):
    query = db.query(models.PhoneNumber)
    return query.all()
