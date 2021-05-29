from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import price as mover_price_schema


def read(db: Session, id: int, user_id):
    query = db.query(models.Price).filter_by(id=id, user_id=user_id)
    return query.first()


def create(db: Session, mover_price: mover_price_schema.MoverPriceCreate, user_id):
    mover_price_db = models.Price(**mover_price.dict(), user_id=user_id)
    db.add(mover_price_db)
    try:
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def read_all(db: Session, user_id):
    query = db.query(models.Price).filter_by(user_id=user_id)
    return query.all()


def delete(db: Session, mover_price_id: int, user_id):
    db.query(models.Price).filter_by(id=mover_price_id, user_id=user_id).delete()
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def update(db: Session, mover_price_id: int, mover_price: mover_price_schema.MoverPriceCreate, user_id):
    db.query(models.Price).filter_by(id=mover_price_id, user_id=user_id).update({**mover_price.dict()})
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
