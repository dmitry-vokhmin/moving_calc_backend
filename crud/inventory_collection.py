from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException, status
from schemas import inventory_collection as inventory_collection_schema
from security.security import get_user, check_privilege


def read(db: Session, move_size_id: int, company_id: int):
    query = db.query(models.InventoryCollection).filter_by(move_size_id=move_size_id, company_id=company_id)
    return query.first()


def create_public(db: Session, inventory_collection: inventory_collection_schema.InventoryCollectionCreate, user_id):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        inventory_collection_db = models.InventoryCollection(**inventory_collection.dict(), is_public=True)
        db.add(inventory_collection_db)
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))


def create_personal(db: Session, inventory_collection: inventory_collection_schema.InventoryCollectionCreate):
    inventory_collection_db = models.InventoryCollection(**inventory_collection.dict(), is_public=False)
    db.add(inventory_collection_db)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return inventory_collection_db


def read_all(db: Session, user_id: int):
    user_db = get_user(db, user_id)
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
        user_collection = create_personal(db, create_schema)
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
           inventory_collection: inventory_collection_schema.InventoryCollectionCreate,
           user_id):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        db.query(models.InventoryCollection).filter_by(id=inventory_collection_id).update(**inventory_collection.dict())
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
