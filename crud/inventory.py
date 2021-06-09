from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import inventory as inventory_schema
from crud.room_collection import read_personal
from security.security import get_user, check_privilege


def read(db: Session, inventory_id: int):
    query = db.query(models.Inventory).filter_by(id=inventory_id)
    return query.first()


def create(db: Session, inventory: inventory_schema.InventoryCreate, user_id: int):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        print(1)
    else:
        check_privilege(db, user_db, "inventory")
        inventory_db = models.Inventory(**inventory.dict(), company_id=user_db.company_id)
        room_collection_db = read_personal(db, user_db.company_id)
        room_collection_db.inventories.append(inventory_db)
        db.add(inventory_db)
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))


def read_all_by_id(db: Session, room_collection_id, inventory_collection_id, user_id: int):
    user_db = get_user(db, user_id)
    check_privilege(db, user_db, "inventory")
    if room_collection_id:
        inventory_db = db.query(models.Inventory).filter(
            models.Inventory.room_collections.any(id=room_collection_id)
        )
    else:
        inventory_db = db.query(models.Inventory).filter(
            models.Inventory.inventory_collections.any(inventory_collection_id=inventory_collection_id)
        )
    return inventory_db.all()
    # query = db.query(models.Inventory).filter((models.Inventory.user_id == user_id) |
    #                                           (models.Inventory.is_public == True))
    # else:
    #     query = db.query(models.Inventory).filter(models.Inventory.inventory_collections.any(
    #         id=db.query(models.InventoryCollection.id).filter(models.InventoryCollection.move_size_id == move_size_id)))
    # else:
    #     query = db.query(models.Inventory).filter(models.Inventory.room_collections.any(name=room_name))
    # return query.all()


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
