from fastapi import Depends, APIRouter, status
from data_base.database import get_db
from schemas import zip_code as zip_code_schema
from crud import zip_code as zip_code_crud
from sqlalchemy.orm import Session
from security.security import get_user_id

router = APIRouter(tags=["Zip code"])


@router.post("/zip_code/", status_code=status.HTTP_201_CREATED)
def create_zip_code(zip_code: zip_code_schema.ZipCodeCreate,
                    db: Session = Depends(get_db),
                    user_id=Depends(get_user_id)):
    zip_code_crud.create(db, zip_code, user_id)


@router.get("/zip_code/", response_model=zip_code_schema.ZipCodeGet, status_code=status.HTTP_200_OK)
def get_zip_code(zip_code: str, db: Session = Depends(get_db)):
    return zip_code_crud.read(db, zip_code)
