from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException, status
from schemas import floor_collection as floor_collection_schema
from security.security import get_user


def read(db: Session, id: int, floor_collection: str):
    if floor_collection:
        query = db.query(models.FloorsCollection).filter(models.FloorsCollection.name == floor_collection)
    else:
        query = db.query(models.FloorsCollection).filter(models.FloorsCollection.id == id)
    return query.first()


def create(db: Session, floor_collection: floor_collection_schema.FloorCollectionCreate, user_id):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        floor_collection_db = models.FloorsCollection(**floor_collection.dict())
        db.add(floor_collection_db)
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
    query = db.query(models.FloorsCollection)
    return query.all()
