from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import address as address_schema
from .street import get_or_create


def read(db: Session, id: int):
    query = db.query(models.Address).filter(models.Address.id == id)
    return query.first()


def create(db: Session, address: address_schema.AddressCreate):
    address_dict = address.dict()
    address_dict["street"] = get_or_create(db, address.street)
    address_db = models.Address(**address_dict)
    db.add(address_db)
    try:
        db.commit()
    except Exception:
        db.rollback()
        address_db = db.query(models.Address).filter_by(**address_dict).first()
    return address_db


def read_all(db: Session):
    query = db.query(models.Address)
    return query.all()
