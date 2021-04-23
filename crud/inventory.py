from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import inventory as inventory_schema


def read(db: Session, id: int, user_id: int):
    query = db.query(models.Inventory).filter_by(id=id, user_id=user_id)
    return query.first()


def create(db: Session, inventory: inventory_schema.InventoryCreate, user_id: int):
    inventory_db = models.Inventory(**inventory.dict(), user_id=user_id)
    db.add(inventory_db)
    try:
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def read_all(db: Session, move_size_id, user_id: int):
    query = db.query(models.Inventory).filter((models.Inventory.user_id == user_id) |
                                              (models.Inventory.is_public == True))
    # else:
    #     query = db.query(models.Inventory).filter(models.Inventory.inventory_collections.any(
    #         id=db.query(models.InventoryCollection.id).filter(models.InventoryCollection.move_size_id == move_size_id)))
    # else:
    #     query = db.query(models.Inventory).filter(models.Inventory.room_collections.any(name=room_name))
    return query.all()


def delete(db: Session, inventory_id: int, user_id: int):
    db.query(models.Inventory).filter_by(id=inventory_id, user_id=user_id).delete()
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def update(db: Session, inventory_id: int, inventory: inventory_schema.InventoryBase, user_id: int):
    db.query(models.Inventory).filter_by(id=inventory_id, user_id=user_id).update({**inventory.dict()})
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
