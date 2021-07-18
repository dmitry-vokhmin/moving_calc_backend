from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException, status
from schemas import zip_code as zip_code_schema
from security.security import get_user


def read(db: Session, zip_code: str):
    query = db.query(models.ZipCode).filter(models.ZipCode.zip_code == zip_code)
    return query.first()


def create(db: Session, zip_code: zip_code_schema.ZipCodeCreate, user_id):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        zip_code_db = models.ZipCode(**zip_code.dict())
        db.add(zip_code_db)
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
