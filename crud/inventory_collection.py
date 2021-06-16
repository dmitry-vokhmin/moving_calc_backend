from typing import List
from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import inventory_collection as inventory_collection_schema
from security.security import get_user, check_privilege
from crud.inventory import read as read_inventory


def read(db: Session, move_size_id: int, company_id: int):
    query = db.query(models.InventoryCollection).filter_by(move_size_id=move_size_id, company_id=company_id)
    return query.first()


def create(db: Session, inventory_collection: inventory_collection_schema.InventoryCollectionCreate):
    inventory_collection_db = models.InventoryCollection(**inventory_collection.dict())
    db.add(inventory_collection_db)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return inventory_collection_db


def add_to_personal(db: Session,
                    inventory_collection: inventory_collection_schema.InventoryCollectionCreatePersonal,
                    user_id: int):
    user_db = get_user(db, user_id)
    check_privilege(db, user_db, "inventory")
    inventory_collection_db = read(db, inventory_collection.move_size_id, user_db.company_id)
    update_or_create(db, inventory_collection.inventory_id, inventory_collection_db.id, inventory_collection.count)
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


# def get_or_create_inventory_collection(db: Session, inventory_collection, company_id):
#     inventory_collection_db = db.query(models.InventoryCollection).filter_by(
#         move_size_id=inventory_collection.move_size_id, company_id=company_id
#     ).first()
#     if not inventory_collection_db:
#         inventory_collection = inventory_collection_schema.InventoryCollectionCreate(
#             move_size_id=inventory_collection.move_size_id,
#             company_id=company_id
#         )
#         inventory_collection_db = create(db, inventory_collection)
#         inventory_collection_id = db.query(models.InventoryCollection).filter_by(
#             move_size_id=inventory_collection.move_size_id, is_public=True).first()
#         inventory_collection_db.inventories.extend(db.query(models.Inventory).filter(
#             models.Inventory.inventory_collections.any(id=inventory_collection_id.id)).all())
#     return inventory_collection_db


# def read_all(db: Session, user_id: int):
#     user_db = get_user(db, user_id)
#     check_privilege(db, user_db, "inventory")
#     user_inventory = db.query(models.InventoryCollection).filter_by(company_id=user_db.company_id).all()
#     if user_inventory:
#         query = db.query(models.InventoryCollection).filter(models.InventoryCollection.move_size_id.notin_(
#             [inventory.move_size_id for inventory in user_inventory]
#         )).all()
#         query.extend(user_inventory)
#     else:
#         query = db.query(models.InventoryCollection).all()
#     return query

def read_all(db: Session, user_id: int):
    user_db = get_user(db, user_id)
    check_privilege(db, user_db, "inventory")
    user_inventory_collection = db.query(models.InventoryCollection).filter_by(company_id=user_db.company_id).all()
    if not user_inventory_collection:
        create_user_collection(db, user_db)
        user_inventory_collection = db.query(models.InventoryCollection).filter_by(company_id=user_db.company_id).all()
    return user_inventory_collection


def create_user_collection(db, user_db):
    for inventory_collection in db.query(models.InventoryCollection).all():
        create_schema = inventory_collection_schema.InventoryCollectionCreate(
            move_size_id=inventory_collection.move_size_id,
            company_id=user_db.company_id
        )
        user_collection = create(db, create_schema)
        create_new_inventory(user_collection, inventory_collection)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def create_new_inventory(user_collection, inventory_collection):
    for row in inventory_collection.inventories:
        new_collection = models.InventoryInventoryCollection(
            inventory_id=row.inventory_id,
            inventory_collection_id=user_collection.id,
            count=row.count
        )
        user_collection.inventories.append(new_collection)


def reset_inventory(db: Session, inventory_collection_id: int, user_id: int):
    user_db = get_user(db, user_id)
    check_privilege(db, user_db, "inventory")
    inventory_collection_db = db.query(models.InventoryCollection).filter_by(id=inventory_collection_id,
                                                                             company_id=user_db.company_id).first()
    inventory_collection_public = db.query(models.InventoryCollection).filter_by(
        move_size_id=inventory_collection_db.move_size_id,
        is_public=True
    ).first()
    db.query(models.InventoryInventoryCollection).filter_by(inventory_collection_id=inventory_collection_id).delete()
    create_new_inventory(inventory_collection_db, inventory_collection_public)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def update(db: Session,
           inventory_collection_id: int,
           inventory_collection: inventory_collection_schema.InventoryCollectionCreate):
    db.query(models.InventoryCollection).filter_by(id=inventory_collection_id).update(**inventory_collection.dict())
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def update_many_to_many_inventory(db: Session, move_size_id: int, inventory: List[int], user_id: int):
    inventory_collection = db.query(models.InventoryCollection).filter_by(move_size_id=move_size_id,
                                                                          user_id=user_id).first()
    inventory_collection.inventories.clear()
    inventory_collection.inventories.extend(db.query(models.Inventory).filter(models.Inventory.id.in_(
        inventory)))
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
