from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import truck_type as truck_type_schema
from security.security import get_user, check_privilege


def read(db: Session, id: int, user_id: int):
    query = db.query(models.TruckType).filter_by(id=id, user_id=user_id)
    return query.first()


def create(db: Session, truck_type: truck_type_schema.TruckTypeCreate, user_id: int):
    user_db = get_user(db, user_id)
    check_privilege(db, user_db, "equipment")
    truck_type_db = models.TruckType(**truck_type.dict(), company_id=user_db.company_id)
    db.add(truck_type_db)
    try:
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def read_all(db: Session, user_id: int):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        query = db.query(models.TruckType)
    else:
        check_privilege(db, user_db, "equipment")
        query = db.query(models.TruckType).filter_by(company_id=user_db.company_id)
    return query.all()


def delete(db: Session, truck_type: truck_type_schema.TruckTypeGet, user_id: int):
    user_db = get_user(db, user_id)
    check_privilege(db, user_db, "equipment")
    db.query(models.TruckType).filter_by(id=truck_type.id, company_id=user_db.company_id).delete()
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def update(db: Session, truck_type: truck_type_schema.TruckTypeUpdate, user_id: int):
    user_db = get_user(db, user_id)
    check_privilege(db, user_db, "equipment")
    db.query(models.TruckType).filter_by(
        id=truck_type.id, company_id=user_db.company_id
    ).update({**truck_type.dict()})
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
