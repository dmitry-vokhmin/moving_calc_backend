from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import address as address_schema


def read(db: Session, id: int):
    query = db.query(models.Address).filter(models.Address.id == id)
    return query.first()


def get_or_create(db: Session, address: address_schema.AddressCreate):
    address_db = models.Address(**address.dict())
    db.add(address_db)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        address_db = db.query(models.Address).filter_by(**address.dict()).first()
    return address_db


def read_all(db: Session):
    query = db.query(models.Address)
    return query.all()
