from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import room_collection as room_collection_schema


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
