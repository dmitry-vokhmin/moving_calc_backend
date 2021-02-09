from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import floor_collection as floor_collection_schema


def read(db: Session, id: int):
    query = db.query(models.FloorsCollection).filter(models.FloorsCollection.id == id)
    return query.first()


def create(db: Session, floor_collection: floor_collection_schema.FloorCollectionCreate):
    floor_collection_db = models.FloorsCollection(**floor_collection.dict())
    db.add(floor_collection_db)
    try:
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e.orig))


def read_all(db: Session):
    query = db.query(models.FloorsCollection)
    return query.all()
