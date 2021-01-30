from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import services as services_schema


def create(db: Session, services: services_schema.ServicesCreate):
    services_db = models.Services(**services.dict())
    db.add(services_db)
    try:
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e.orig))

def read_all(db: Session):
    query = db.query(models.Services)
    return query.all()
