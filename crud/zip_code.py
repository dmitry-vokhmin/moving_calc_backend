from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import zip_code as zip_code_schema


def read(db: Session, zip_code: str):
    query = db.query(models.ZipCode).filter(models.ZipCode.zip_code == zip_code)
    return query.first()


def create(db: Session, zip_code: zip_code_schema.ZipCodeCreate):
    zip_code_db = models.ZipCode(**zip_code.dict())
    db.add(zip_code_db)
    try:
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def read_all(db: Session):
    query = db.query(models.ZipCode)
    return query.all()
