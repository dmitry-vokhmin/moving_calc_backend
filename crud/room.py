from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException, status
from schemas import room as room_schema
from security.security import get_user


def read(db: Session, room_name: str):
    query = db.query(models.Room).filter_by(name=room_name)
    return query.first()


def create(db: Session, room: room_schema.RoomCreate, user_id):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        room_db = models.Room(**room.dict())
        db.add(room_db)
        try:
            db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        return room_db
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def create_room_category(db: Session, room_category: room_schema.RoomCategoryCreate, user_id):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        room_db = db.query(models.Room).filter_by(id=room_category.room_id).first()
        room_db.inventory_category.append(
            db.query(models.InventoryCategory).filter_by(id=room_category.category_id).first()
        )
        try:
            db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def read_all(db: Session):
    query = db.query(models.Room)
    return query.all()


def delete(db: Session, room_id, user_id):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        db.query(models.InventoryCategory).filter_by(id=room_id, user_id=user_id).delete()
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def update(db: Session, room_id, room, user_id):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        db.query(models.PriceTag).filter_by(id=room_id, user_id=user_id).update(
            {**room.dict()}
        )
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
