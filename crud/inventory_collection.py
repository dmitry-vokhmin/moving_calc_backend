from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import inventory_collection as inventory_collection_schema


def read(db: Session, id: int):
    query = db.query(models.InventoryCollection).filter(models.InventoryCollection.id == id)
    return query.first()


def create(db: Session, inventory_collection: inventory_collection_schema.InventoryCollectionCreate):
    inventory_collection_db = models.InventoryCollection(move_size_id=inventory_collection.move_size_id)
    db.add(inventory_collection_db)
    try:
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e.orig))


def read_all(db: Session):
    query = db.query(models.InventoryCollection)
    return query.all()


def create_many_to_many_inventory(db: Session, move_size_id, inventory_list):
    inventory_collection = db.query(models.InventoryCollection).filter_by(id=move_size_id).first()
    inventory = db.query(models.Inventory).filter(models.Inventory.id.in_(
        db.query(models.Inventory.id).filter(models.Inventory.name.in_(inventory_list)))).all()
    inventory_collection.inventories.extend(inventory)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e.orig))
