from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import order as order_schema

def read(db: Session, id: int):
    query = db.query(models.Order).filter(models.Order.id == id)
    return query.first()

def create(db: Session, order: order_schema.OrderCreate):
    order_db = models.Order(**order.dict())
    db.add(order_db)
    try:
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e.orig))
