from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException, status
from schemas import price_tag as price_tag_schema
from security.security import get_user


def create(db: Session, price_tag: price_tag_schema.PriceTagCreate, user_id: int):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        price_tag_db = models.PriceTag(**price_tag.dict(), user_id=user_id)
        db.add(price_tag_db)
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def read_all(db: Session):
    query = db.query(models.PriceTag)
    return query.all()


def delete(db: Session, price_tag_id: int, user_id: int):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        db.query(models.PriceTag).filter_by(id=price_tag_id, user_id=user_id).delete()
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def update(db: Session, price_tag_id: int, price_tag: price_tag_schema.PriceTagCreate, user_id: int):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        db.query(models.PriceTag).filter_by(id=price_tag_id, user_id=user_id).update({**price_tag.dict()})
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
