from sqlalchemy.orm import Session
from fastapi import HTTPException
from data_base import models
from schemas import mover_amount as mover_amount_schema


def read(db: Session, id: int):
    query = db.query(models.MoverAmount).filter(models.MoverAmount.id == id)
    return query.first()


def create(db: Session, mover_amount: mover_amount_schema.MoverAmountCreate):
    mover_amount_db = models.MoverAmount(**mover_amount.dict())
    db.add(mover_amount_db)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def read_all(db: Session):
    query = db.query(models.MoverAmount)
    return query.all()


def delete(db: Session, mover_amount_id: int):
    db.query(models.MoverAmount).filter_by(id=mover_amount_id).delete()
    try:
        db.commit()
    except HTTPException as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def update(db: Session, mover_amount_id: int, mover_amount: mover_amount_schema.MoverAmountBase):
    db.query(models.MoverAmount).filter_by(id=mover_amount_id).update({"amount": mover_amount.amount})
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
