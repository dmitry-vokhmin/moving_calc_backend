from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from security.security import get_user, check_privilege
from schemas import inventory_inventory_collection as inventory_inventory_collection_schema


def create_public(db: Session,
                  inventory_collection: inventory_inventory_collection_schema.InventoryInventoryCollectionCreate):
    new_inventory_inventory_collection_db = models.InventoryInventoryCollection(**inventory_collection.dict())
    db.add(new_inventory_inventory_collection_db)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def create(db: Session,
           inventory_collection: inventory_inventory_collection_schema.InventoryInventoryCollectionCreate,
           user_id: int):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        create_public(db, inventory_collection)
    else:
        create_personal(db, inventory_collection, user_db)


def create_personal(db: Session,
                    inventory_collection: inventory_inventory_collection_schema.InventoryInventoryCollectionCreate,
                    user_db):
    check_privilege(db, user_db, "inventory")
    update_or_create(db,
                     inventory_collection.inventory_id,
                     inventory_collection.inventory_collection_id,
                     inventory_collection.count)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def update_or_create(db: Session, inventory_id, inventory_collection_id, count):
    inventory_inventory_collection_db = db.query(models.InventoryInventoryCollection).filter_by(
        inventory_id=inventory_id,
        inventory_collection_id=inventory_collection_id
    )
    if inventory_inventory_collection_db.first():
        db_count = inventory_inventory_collection_db.first().count
        inventory_inventory_collection_db.update({"count": db_count + count})
    else:
        new_inventory_inventory_collection_db = models.InventoryInventoryCollection(
            inventory_id=inventory_id,
            inventory_collection_id=inventory_collection_id,
            count=count
        )
        db.add(new_inventory_inventory_collection_db)


def read_all(db: Session, inventory_collection_id: int, move_size_id: int, user_id: int):
    user_db = get_user(db, user_id)
    if move_size_id:
        inventory_collection_db = db.query(models.InventoryCollection).filter_by(move_size_id=move_size_id,
                                                                                 company_id=user_db.company_id).first()
        inventory_collection_id = inventory_collection_db.id
    query = db.query(models.InventoryInventoryCollection).filter_by(inventory_collection_id=inventory_collection_id)
    return query.all()


def bulk_update(db: Session,
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
