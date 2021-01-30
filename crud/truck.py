from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import truck as truck_schema

def read(db: Session, id: int):
    query = db.query(models.Truck).filter(models.Truck.id == id)
    return query.first()

def create(db: Session, truck: truck_schema.TruckCreate):
    truck_db = models.Truck(name=truck.name)
    db.add(truck_db)
    try:
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e.orig))

def read_all(db: Session):
    query = db.query(models.Truck)
    return query.all()
