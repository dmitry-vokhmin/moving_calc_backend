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
        raise HTTPException(status_code=400, detail=str(e))


def read_all(db: Session, move_size_id):
    if move_size_id == "all":
        query = db.query(models.Inventory)
    else:
        query = db.query(models.Inventory).filter(models.Inventory.inventory_collections.any(
            id=db.query(models.InventoryCollection.id).filter(models.InventoryCollection.move_size_id == move_size_id)))
    # else:
    #     query = db.query(models.Inventory).filter(models.Inventory.room_collections.any(name=room_name))
    return query.all()
