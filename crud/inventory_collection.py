from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import inventory_collection as inventory_collection_schema


def read(db: Session, id: int):
    query = db.query(models.InventoryCollection).filter(models.InventoryCollection.id == id)
    return query.first()


def create(db: Session, inventory_collection: inventory_collection_schema.InventoryCollectionCreate):
    inventory_collection_db = models.InventoryCollection(preset=inventory_collection.preset)
    db.add(inventory_collection_db)
    try:
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e.orig))


def read_all(db: Session):
    query = db.query(models.InventoryCollection)
    return query.all()
