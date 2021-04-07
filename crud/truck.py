from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import truck as truck_schema


def read(db: Session, id: int):
    query = db.query(models.Truck).filter(models.Truck.id == id)
    return query.first()


def create(db: Session, truck: truck_schema.TruckCreate):
    truck_db = models.Truck(**truck.dict())
    db.add(truck_db)
    try:
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def read_all(db: Session):
    query = db.query(models.Truck)
    return query.all()


def delete(db: Session, truck_id: int):
    db.query(models.Truck).filter_by(id=truck_id).delete()
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def update(db: Session, truck_id: int, truck: truck_schema.TruckBase):
    db.query(models.Truck).filter_by(id=truck_id).update({**truck.dict()})
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
