from typing import List
from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from data_base.database import get_db
from schemas import company as company_schema
from crud import company as company_crud
from security.security import get_user_id
from data_base.models import User


router = APIRouter(tags=["Company"])


@router.post("/company/", status_code=status.HTTP_201_CREATED)
def post_company(company: company_schema.CompanyCreate,
                 db: Session = Depends(get_db),
                 user: User = Depends(get_user_id)):
    if user.is_staff:
        company_crud.create(db, company)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/company/", response_model=company_schema.CompanyGet, status_code=status.HTTP_200_OK)
def read_company(db: Session = Depends(get_db), user: User = Depends(get_user_id)):
    return company_crud.read(db, user.company_id)


@router.get("/company/all/", response_model=List[company_schema.CompanyGet], status_code=status.HTTP_200_OK)
def read_all_companies(db: Session = Depends(get_db), user: User = Depends(get_user_id)):
    if user.is_staff:
        return company_crud.read_all(db)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
