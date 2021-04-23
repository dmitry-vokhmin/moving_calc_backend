from sqlalchemy.orm import Session
from fastapi import HTTPException
from data_base import models
from schemas import company as company_schema


def read(db: Session, user_company_id: int):
    query = db.query(models.Company).filter_by(id=user_company_id)
    return query.first()


def create(db: Session, company: company_schema.CompanyCreate):
    company_db = models.Company(**company.dict())
    db.add(company_db)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def read_all(db: Session):
    query = db.query(models.Company)
    return query.all()


def delete(db: Session, company_id: int):
    db.query(models.Company).filter_by(id=company_id).delete()
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def update(db: Session, company_id: int, company: company_schema.CompanyBase):
    db.query(models.Company).filter_by(id=company_id).update({**company.dict()})
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
