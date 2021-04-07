from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import price_tag as price_tag_schema


def read(db: Session, id: int):
    query = db.query(models.PriceTag).filter(models.PriceTag.id == id)
    return query.first()


def create(db: Session, price_tag: price_tag_schema.PriceTagCreate):
    price_tag_db = models.PriceTag(**price_tag.dict())
    db.add(price_tag_db)
    try:
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def read_all(db: Session):
    query = db.query(models.PriceTag)
    return query.all()


def delete(db: Session, price_tag_id: int):
    db.query(models.PriceTag).filter_by(id=price_tag_id).delete()
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def update(db: Session, price_tag_id: int, price_tag: price_tag_schema.PriceTagBase):
    db.query(models.PriceTag).filter_by(id=price_tag_id).update({"price": price_tag.price})
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
