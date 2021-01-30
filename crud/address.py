from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import address as address_schema

def read(db: Session, id: int):
    query = db.query(models.Address).filter(models.Address.id == id)
    return query.first()

def create(db: Session, address: address_schema.AddressCreate):
    address_db = models.Address(**address.dict())
    db.add(address_db)
    try:
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e.orig))

def read_all(db: Session):
    query = db.query(models.Address)
    return query.all()
