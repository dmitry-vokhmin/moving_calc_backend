from typing import List
from fastapi import Depends, APIRouter, status, HTTPException
from data_base.database import get_db
from schemas import price_tag as price_tag_schema
from crud import price_tag as price_tag_crud
from sqlalchemy.orm import Session
from security.security import get_current_user
from data_base.models import User

router = APIRouter(tags=["Price tag"])


@router.post("/price_tag/", status_code=status.HTTP_201_CREATED)
def create_price_tag(price_tag: price_tag_schema.PriceTagCreate,
                     db: Session = Depends(get_db),
                     user: User = Depends(get_current_user)):
    price_tag_crud.create(db, price_tag, user.id)


@router.get("/price_tag/{price_tag_id}",
            response_model=price_tag_schema.PriceTagGet,
            status_code=status.HTTP_200_OK)
def get_price_tag(price_tag_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return price_tag_crud.read(db, price_tag_id, user.id)


@router.get("/price_tag/", response_model=List[price_tag_schema.PriceTagGet], status_code=status.HTTP_200_OK)
def get_all_price_tags(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return price_tag_crud.read_all(db, user.id)


@router.put("/price_tag/delete/{price_tag_id}", status_code=status.HTTP_200_OK)
def delete_price_tag(price_tag_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    price_tag_crud.delete(db, price_tag_id, user.id)


@router.put("/price_tag/update/{price_tag_id}", status_code=status.HTTP_200_OK)
def update_price_tag(
        price_tag_id: int,
        price_tag: price_tag_schema.PriceTagCreate,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)):
    price_tag_crud.update(db, price_tag_id, price_tag, user.id)
