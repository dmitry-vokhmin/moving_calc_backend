from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import inventory_category as inventory_category_schema
from security.security import get_user, check_privilege


def read(db: Session, id: int, user_id: int):
    user_db = get_user(db, user_id)
    check_privilege(db, user_db, "inventory")
    category_db = db.query(models.InventoryCategory)
    return category_db.first()


def create(db: Session, inventory_category: inventory_category_schema.InventoryCategoryCreate):
    inventory_category_db = models.InventoryCategory(name=inventory_category.name)
    db.add(inventory_category_db)
    try:
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def read_all(db: Session, user_id: int, room_id: int):
    user_db = get_user(db, user_id)
    check_privilege(db, user_db, "inventory")
    if room_id:
        category_db = db.query(models.InventoryCategory).filter(
            models.InventoryCategory.room.any(id=room_id)
        )
    else:
        category_db = db.query(models.InventoryCategory)
    return category_db.all()
