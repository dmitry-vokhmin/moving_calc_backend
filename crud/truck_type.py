from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import truck_type as truck_type_schema

def read(db: Session, id: int):
    query = db.query(models.TruckType).filter(models.TruckType.id == id)
    return query.first()

def create(db: Session, truck_type: truck_type_schema.TruckTypeCreate):
    truck_type_db = models.TruckType(**truck_type.dict())
    db.add(truck_type_db)
    try:
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e.orig))

def read_all(db: Session):
    query = db.query(models.TruckType)
    return query.all()
