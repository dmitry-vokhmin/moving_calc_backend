from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import user as user_schema

def read(db: Session, id: int):
    query = db.query(models.User).filter(models.User.id == id)
    return query.first()

def get_or_create(db: Session, user: user_schema.UserCreate):
    # phone_number = db.query(models.PhoneNumber).filter(models.PhoneNumber.phone_number == user.phone_number).first()
    user_db = models.User(**user.dict())
    db.add(user_db)
    try:
        db.commit()
    except Exception:
        db.rollback()
        user_db = db.query(models.User).filter_by(**user.dict()).first()
    return user_db
