from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import room_collection as room_collection_schema


def read(db: Session, id: int):
    query = db.query(models.RoomCollection).filter(models.RoomCollection.id == id)
    return query.first()


def create(db: Session, room_collection: room_collection_schema.RoomCollectionsCreate):
    room_collection_db = models.RoomCollection(name=room_collection.name)
    db.add(room_collection_db)
    try:
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e.orig))


def read_all(db: Session):
    query = db.query(models.RoomCollection)
    return query.all()


def create_many_to_many_inventory(db: Session, room_id, inventory_list):
    room_collection = db.query(models.RoomCollection).filter_by(id=room_id).first()
    inventory = db.query(models.Inventory).filter(models.Inventory.id.in_(
        db.query(models.Inventory.id).filter(models.Inventory.name.in_(inventory_list)))).all()
    room_collection.inventories.extend(inventory)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e.orig))