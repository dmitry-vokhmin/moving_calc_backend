from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import mover_price as mover_price_schema


def read(db: Session, id: int):
    query = db.query(models.MoverPrice).filter(models.MoverPrice.id == id)
    return query.first()


def create(db: Session, mover_price: mover_price_schema.MoverPriceCreate):
    mover_price_db = models.MoverPrice(**mover_price.dict())
    db.add(mover_price_db)
    try:
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e.orig))


def read_all(db: Session):
    query = db.query(models.MoverPrice)
    return query.all()


def update(db: Session, mover_price: mover_price_schema.MoverPriceBase):
    db.query(models.MoverPrice).filter_by(movers=mover_price.movers).update({"price": mover_price.price})
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e.orig))