from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException, status
from schemas import inventory_category as inventory_category_schema
from security.security import get_user


def create(db: Session, inventory_category: inventory_category_schema.InventoryCategoryCreate, user_id):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        inventory_category_db = models.InventoryCategory(name=inventory_category.name)
        db.add(inventory_category_db)
        try:
            db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def read_all(db: Session, room_id: int):
    if room_id:
        category_db = db.query(models.InventoryCategory).filter(
            models.InventoryCategory.room.any(id=room_id)
        )
    else:
        category_db = db.query(models.InventoryCategory)
    return category_db.all()


def delete(db: Session, inventory_category_id, user_id):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        db.query(models.InventoryCategory).filter_by(id=inventory_category_id, user_id=user_id).delete()
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def update(db: Session, inventory_category_id, inventory_category, user_id):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        db.query(models.PriceTag).filter_by(id=inventory_category_id, user_id=user_id).update(
            {**inventory_category.dict()}
        )
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
