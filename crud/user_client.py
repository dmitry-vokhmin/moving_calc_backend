from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException, status
from schemas import user_client as user_client_schema
from security.security import get_user


def read(db: Session, id: int, user_id):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        query = db.query(models.UserClient).filter(models.UserClient.id == id)
        return query.first()
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_or_create(db: Session, user: user_client_schema.UserCreate):
    user_db = models.UserClient(**user.dict())
    db.add(user_db)
    try:
        db.commit()
    except Exception:
        db.rollback()
        user_db = db.query(models.UserClient).filter_by(**user.dict()).first()
    return user_db


def read_all(db: Session, user_id):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        query = db.query(models.UserClient)
        return query.all()
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
