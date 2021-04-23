from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import user as user_schema
from security.security import get_secret_hash


def create(db: Session, user: user_schema.UserCreate):
    user_db = models.User(
        username=user.username,
        email=user.email,
        password=get_secret_hash(user.password.get_secret_value()),
        company_id=user.company_id
    )
    db.add(user_db)
    try:
        db.commit()
    except Exception:
        # TODO: выдавать ошибку пользователю при регистрации
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid user")
    return user_db


def read(db: Session, user_id: int):
    user_db = db.query(models.User).filter_by(id=user_id).first()
    return user_db


def read_by_user_name(db: Session, user: user_schema.UserAuth):
    user_db = db.query(models.User).filter_by(username=user.username).first()
    return user_db
