from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import move_size as move_size_schema


def read(db: Session, id: int):
    query = db.query(models.MoveSize).filter(models.MoveSize.id == id)
    return query.first()


def create(db: Session, move_size: move_size_schema.MoveSizeCreate):
    move_size_db = models.MoveSize(name=move_size.name)
    db.add(move_size_db)
    try:
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e.orig))


def read_all(db: Session):
    query = db.query(models.MoveSize)
    return query.all()
