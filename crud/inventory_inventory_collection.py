from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from security.security import get_user, check_privilege
from schemas import inventory_inventory_collection as inventory_inventory_collection_schema


def read_all(db: Session, inventory_collection_id: int, user_id: int):
    user_db = get_user(db, user_id)
    check_privilege(db, user_db, "inventory")
    query = db.query(models.InventoryInventoryCollection).filter_by(inventory_collection_id=inventory_collection_id)
    return query.all()


def update(db: Session,
           inventory_collection: inventory_inventory_collection_schema.InventoryInventoryCollectionUpdate,
           user_id: int):
    user_db = get_user(db, user_id)
    check_privilege(db, user_db, "inventory")
    for inventory_collection in inventory_collection.__root__:
        db.query(models.InventoryInventoryCollection).filter_by(
            inventory_id=inventory_collection.inventory_id,
            inventory_collection_id=inventory_collection.inventory_collection_id
        ).update({"count": inventory_collection.count})
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))


def delete_inventory(db: Session,
                     inventory_collection: inventory_inventory_collection_schema.InventoryInventoryCollectionDelete,
                     user_id: int):
    user_db = get_user(db, user_id)
    check_privilege(db, user_db, "inventory")
    db.query(models.InventoryInventoryCollection).filter_by(
        inventory_id=inventory_collection.inventory_id,
        inventory_collection_id=inventory_collection.inventory_collection_id).delete()
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
