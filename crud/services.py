from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import services as services_schema


def read(db: Session, id: int, service: str):
    if service:
        query = db.query(models.Service).filter(models.Service.name == service)
    else:
        query = db.query(models.Service).filter(models.Service.id == id)
    return query.first()


def create(db: Session, services: services_schema.ServicesCreate):
    services_db = models.Service(**services.dict())
    db.add(services_db)
    try:
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def read_all(db: Session):
    query = db.query(models.Service)
    return query.all()


def delete(db: Session, service_id: int):
    db.query(models.Service).filter_by(id=service_id).delete()
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def update(db: Session, service_id: int, service: services_schema.ServicesBase):
    db.query(models.Service).filter_by(id=service_id).update({"name": service.name})
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
