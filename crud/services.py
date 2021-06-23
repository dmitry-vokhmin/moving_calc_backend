from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException, status
from schemas import services as services_schema
from security.security import get_user


def create(db: Session, services: services_schema.ServicesCreate, user_id):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        services_db = models.Service(**services.dict())
        db.add(services_db)
        try:
            db.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def read_all(db: Session):
    query = db.query(models.Service)
    return query.all()


def delete(db: Session, service_id: int, user_id):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        db.query(models.Service).filter_by(id=service_id).delete()
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def update(db: Session, service_id: int, service: services_schema.ServicesBase, user_id):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        db.query(models.Service).filter_by(id=service_id).update({"name": service.name})
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
