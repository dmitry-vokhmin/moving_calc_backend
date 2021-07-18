from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session
from data_base.database import get_db
from schemas import company as company_schema
from crud import company as company_crud
from security.security import get_user_id

router = APIRouter(tags=["Company"])


@router.post("/company/", response_model=company_schema.CompanyGet, status_code=status.HTTP_201_CREATED)
def post_company(company: company_schema.CompanyCreate,
                 db: Session = Depends(get_db)):
    return company_crud.create(db, company)


@router.put("/company/", status_code=status.HTTP_200_OK)
def update_company(company: company_schema.CompanyCreate,
                   db: Session = Depends(get_db),
                   user_id=Depends(get_user_id)):
    company_crud.update(db, company, user_id)
