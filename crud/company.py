from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from data_base import models
from schemas import company as company_schema
from security.security import get_user
from schemas.address import AddressCreate
from crud.zip_code import read as read_zip_code
from crud.address import get_or_create as get_or_create_address


def create(db: Session, company: company_schema.CompanyCreate):
    zip_code_id = get_zip_code(db, company.zip_code)
    address_schema = AddressCreate(street=company.street,
                                   apartment=company.apartment,
                                   zip_code_id=zip_code_id)
    address_db = get_or_create_address(db, address_schema)
    company_db = models.Company(name=company.name, address_id=address_db.id, is_active=False)
    db.add(company_db)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return company_db


def update(db: Session, company: company_schema.CompanyCreate, user_id):
    zip_code_id = get_zip_code(db, company.zip_code)
    address_schema = AddressCreate(street=company.street,
                                   apartment=company.apartment,
                                   zip_code_id=zip_code_id)
    address_db = get_or_create_address(db, address_schema)
    user_db = get_user(db, user_id)
    company_db = db.query(models.Company).filter_by(id=user_db.company_id)
    company_db.update({"name": company.name, "address_id": address_db.id})
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def get_zip_code(db: Session, zip_code):
    zip_code_db = read_zip_code(db, zip_code)
    if zip_code_db:
        return zip_code_db.id
    raise HTTPException(status_code=400, detail=str("Zip code does not exist"))


def read_all(db: Session, user_id):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        query = db.query(models.Company)
        return query.all()
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
