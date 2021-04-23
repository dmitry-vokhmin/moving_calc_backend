from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import truck_type as truck_type_schema


def read(db: Session, id: int, user_id: int):
    query = db.query(models.TruckType).filter_by(id=id, user_id=user_id)
    return query.first()


def create(db: Session, truck_type: truck_type_schema.TruckTypeCreate, user_id: int):
    truck_type_db = models.TruckType(**truck_type.dict(), user_id=user_id)
    db.add(truck_type_db)
    try:
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def read_all(db: Session, user_id: int):
    query = db.query(models.TruckType).filter_by(user_id=user_id)
    return query.all()


def delete(db: Session, truck_type_id: int, user_id: int):
    db.query(models.TruckType).filter_by(id=truck_type_id, user_id=user_id).delete()
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def update(db: Session, truck_type_id: int, truck_type: truck_type_schema.TruckTypeBase, user_id: int):
    db.query(models.TruckType).filter_by(id=truck_type_id, user_id=user_id).update({**truck_type.dict()})
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
