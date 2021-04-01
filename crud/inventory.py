from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import inventory as inventory_schema


def read(db: Session, id: int):
    query = db.query(models.Inventory).filter(models.Inventory.id == id)
    return query.first()


def create(db: Session, inventory: inventory_schema.InventoryCreate):
    inventory_db = models.Inventory(**inventory.dict())
    db.add(inventory_db)
    try:
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e.orig))


def read_all(db: Session, room_name):
    if room_name == "all":
        query = db.query(models.Inventory)
    elif room_name == "1bd":
        query = db.query(models.Inventory).filter(models.Inventory.inventory_collections.any(
            id=db.query(models.InventoryCollection.id).filter(models.InventoryCollection.move_size_id == (
                db.query(models.MoveSize.id).filter(models.MoveSize.name == room_name)))))
    else:
        query = db.query(models.Inventory).filter(models.Inventory.room_collections.any(name=room_name))
    return query.all()
