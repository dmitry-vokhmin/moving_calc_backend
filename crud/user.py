from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import user as user_schema

def read(db: Session, id: int):
    query = db.query(models.User).filter(models.User.id == id)
    return query.first()

def create(db: Session, user: user_schema.UserCreate):
    user_db = models.User(**user.dict())
    db.add(user_db)
    try:
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e.orig))
