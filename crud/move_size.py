from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException, status
from schemas import move_size as move_size_schema
from security.security import get_user


def create(db: Session, move_size: move_size_schema.MoveSizeCreate, user_id):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        move_size_db = models.MoveSize(**move_size.dict())
        db.add(move_size_db)
        try:
            db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def read_all(db: Session):
    query = db.query(models.MoveSize)
    return query.all()


def delete(db: Session, move_size_id: int, user_id):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        db.query(models.Service).filter_by(id=move_size_id).delete()
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def update(db: Session, move_size_id: int, move_size: move_size_schema.MoveSizeCreate, user_id):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        db.query(models.Service).filter_by(id=move_size_id).update({**move_size.dict()})
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
