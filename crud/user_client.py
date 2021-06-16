from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import user_client as user_client_schema


def read(db: Session, id: int):
    query = db.query(models.UserClient).filter(models.UserClient.id == id)
    return query.first()


def get_or_create(db: Session, user: user_client_schema.UserCreate):
    user_db = models.UserClient(**user.dict())
    db.add(user_db)
    try:
        db.commit()
    except Exception:
        db.rollback()
        user_db = db.query(models.UserClient).filter_by(**user.dict()).first()
    return user_db


def read_all(db: Session):
    query = db.query(models.UserClient)
    return query.all()
