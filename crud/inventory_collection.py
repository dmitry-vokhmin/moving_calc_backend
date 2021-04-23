from typing import List
from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import inventory_collection as inventory_collection_schema


def read(db: Session, id: int, user_id: int):
    query = db.query(models.InventoryCollection).filter_by(id=id, user_id=user_id)
    return query.first()


def create(db: Session, inventory_collection: inventory_collection_schema.InventoryCollectionCreate):
    inventory_collection_db = models.InventoryCollection(**inventory_collection.dict())
    db.add(inventory_collection_db)
    try:
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def read_all(db: Session, user_id: int):
    query = db.query(models.InventoryCollection).filter_by(user_id=user_id)
    return query.all()


def delete(db: Session, inventory_collection_id: int):
    db.query(models.InventoryCollection).filter_by(id=inventory_collection_id).delete()
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def update(db: Session,
           inventory_collection_id: int,
           inventory_collection: inventory_collection_schema.InventoryCollectionCreate):
    db.query(models.InventoryCollection).filter_by(id=inventory_collection_id).update(**inventory_collection.dict())
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def update_many_to_many_inventory(db: Session, move_size_id: int, inventory: List[int], user_id: int):
    inventory_collection = db.query(models.InventoryCollection).filter_by(move_size_id=move_size_id,
                                                                          user_id=user_id).first()
    inventory_collection.inventories.clear()
    inventory_collection.inventories.extend(db.query(models.Inventory).filter(models.Inventory.id.in_(
        inventory)))
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
