from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import price_tag_name as price_tag_name_schema


def read(db: Session, id: int):
    query = db.query(models.PriceTagName).filter(models.PriceTagName.id == id)
    return query.first()


def create(db: Session, price_tag_name: price_tag_name_schema.PriceTagNameCreate):
    price_tag_db = models.PriceTagName(**price_tag_name.dict())
    db.add(price_tag_db)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def read_all(db: Session):
    query = db.query(models.PriceTagName)
    return query.all()


def delete(db: Session, price_tag_name_id: int):
    db.query(models.PriceTagName).filter_by(id=price_tag_name_id).delete()
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def update(db: Session, price_tag_name_id: int, price_tag_name: price_tag_name_schema.PriceTagNameBase):
    db.query(models.PriceTagName).filter_by(id=price_tag_name_id).update({"name": price_tag_name.name})
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
