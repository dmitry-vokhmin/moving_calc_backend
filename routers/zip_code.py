from typing import List
from fastapi import Depends, APIRouter, status, HTTPException
from data_base.database import get_db
from schemas import zip_code as zip_code_schema
from crud import zip_code as zip_code_crud
from sqlalchemy.orm import Session
from security.security import get_current_user
from data_base.models import User

router = APIRouter(tags=["Zip code"])


@router.post("/zip_code/", status_code=status.HTTP_201_CREATED)
def create_zip_code(zip_code: zip_code_schema.ZipCodeCreate,
                    db: Session = Depends(get_db),
                    user: User = Depends(get_current_user)):
    if user.is_staff:
        zip_code_crud.create(db, zip_code)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/zip_code/{zip_code_id}", response_model=zip_code_schema.ZipCodeGet, status_code=status.HTTP_200_OK)
def get_zip_code(zip_code_id: int, q: str = None, db: Session = Depends(get_db)):
    return zip_code_crud.read(db, zip_code_id, q)


@router.get("/zip_code/", response_model=List[zip_code_schema.ZipCodeGet], status_code=status.HTTP_200_OK)
def get_all_zip_code(db: Session = Depends(get_db)):
    return zip_code_crud.read_all(db)
