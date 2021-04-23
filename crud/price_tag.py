from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import price_tag as price_tag_schema


def read(db: Session, id: int, user_id: int):
    query = db.query(models.PriceTag).filter_by(id=id, user_id=user_id)
    return query.first()


def create(db: Session, price_tag: price_tag_schema.PriceTagCreate, user_id: int):
    price_tag_db = models.PriceTag(**price_tag.dict(), user_id=user_id)
    db.add(price_tag_db)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def read_all(db: Session, user_id: int):
    query = db.query(models.PriceTag).filter_by(user_id=user_id)
    return query.all()


def delete(db: Session, price_tag_id: int, user_id: int):
    db.query(models.PriceTag).filter_by(id=price_tag_id, user_id=user_id).delete()
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def update(db: Session, price_tag_id: int, price_tag: price_tag_schema.PriceTagCreate, user_id: int):
    db.query(models.PriceTag).filter_by(id=price_tag_id, user_id=user_id).update({**price_tag.dict()})
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
