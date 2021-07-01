from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException, status
from schemas import order as order_schema
from security.security import get_user


def read(db: Session, id: int, user_id):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        query = db.query(models.Order).filter(models.Order.id == id)
        return query.first()
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def create(db: Session, order: order_schema.OrderCreate):
    order_db = models.Order(**order.dict(exclude={"move_size_id_list"}))
    order_db.move_sizes.extend(db.query(models.MoveSize).filter(models.MoveSize.id.in_(order.move_size_id_list)).all())
    db.add(order_db)
    try:
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return order_db


def read_all(db: Session, user_id):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        query = db.query(models.Order)
        return query.all()
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
