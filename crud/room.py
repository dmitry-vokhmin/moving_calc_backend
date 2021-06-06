from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import room as room_schema


def read(db: Session, room_name: str):
    query = db.query(models.Room).filter_by(name=room_name)
    return query.first()


def create(db: Session, room: room_schema.RoomCreate):
    room_db = models.Room(name=room.name)
    db.add(room_db)
    try:
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def read_all(db: Session):
    query = db.query(models.Room)
    return query.all()
