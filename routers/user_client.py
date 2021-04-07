from typing import List
from fastapi import Depends, APIRouter, status
from data_base.database import get_db
from schemas import user_client as user_client_schema
from crud import user_client as user_client_crud
from sqlalchemy.orm import Session

router = APIRouter(tags=["User Client"])


@router.post("/user_client/", response_model=user_client_schema.UserGet, status_code=status.HTTP_201_CREATED)
def create_user(user: user_client_schema.UserCreate, db: Session = Depends(get_db)):
    return user_client_crud.get_or_create(db, user)


@router.get("/user_client/{user_client_id}", response_model=user_client_schema.UserGet, status_code=status.HTTP_200_OK)
def get_user(user_client_id: int, db: Session = Depends(get_db)):
    return user_client_crud.read(db, user_client_id)


@router.get("/user_client/", response_model=List[user_client_schema.UserGet], status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db)):
    return user_client_crud.read_all(db)
