from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from data_base import models
from schemas import mover_amount as mover_amount_schema
from security.security import get_user


def create(db: Session, mover_amount: mover_amount_schema.MoverAmountCreate, user_id):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        mover_amount_db = models.MoverAmount(**mover_amount.dict())
        db.add(mover_amount_db)
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


def read_all(db: Session):
    query = db.query(models.MoverAmount)
    return query.all()


def delete(db: Session, mover_amount_id: int, user_id):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        db.query(models.MoverAmount).filter_by(id=mover_amount_id).delete()
        try:
            db.commit()
        except HTTPException as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def update(db: Session, mover_amount_id: int, mover_amount: mover_amount_schema.MoverAmountBase, user_id):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        db.query(models.MoverAmount).filter_by(id=mover_amount_id).update({"amount": mover_amount.amount})
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
