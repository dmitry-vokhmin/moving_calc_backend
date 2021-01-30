from typing import List
from fastapi import Depends, APIRouter, status
from data_base.database import get_db
from schemas import user as user_schema
from crud import user as user_crud
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/user/", status_code=status.HTTP_201_CREATED)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    user_crud.create(db, user)

@router.get("/user/{user_id}", response_model=List[user_schema.UserGet], status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_crud.read(db, user_id)