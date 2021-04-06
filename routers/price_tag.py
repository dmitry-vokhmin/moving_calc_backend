from typing import List
from fastapi import Depends, APIRouter, status
from data_base.database import get_db
from data_base import models
from schemas import price_tag as price_tag_schema
from crud import price_tag as price_tag_crud
from sqlalchemy.orm import Session

router = APIRouter(tags=["Price tag"])


@router.post("/price_tag/", status_code=status.HTTP_201_CREATED)
def create_price_tag(price_tag: price_tag_schema.PriceTagCreate, db: Session = Depends(get_db)):
    price_tag_crud.create(db, price_tag)


@router.get("/price_tag/{price_tag_id}",
            response_model=price_tag_schema.PriceTagGet,
            status_code=status.HTTP_200_OK)
def get_price_tag(price_tag_id: int, db: Session = Depends(get_db)):
    return price_tag_crud.read(db, price_tag_id)


@router.get("/price_tag/", response_model=List[price_tag_schema.PriceTagGet], status_code=status.HTTP_200_OK)
def get_all_price_tags(db: Session = Depends(get_db)):
    return price_tag_crud.read_all(db)


@router.put("/price_tag/{price_tag_id}", status_code=status.HTTP_200_OK)
def delete_update_price_tag(price_tag_id: int, q: str, price_tag: price_tag_schema.PriceTagBase,
                            db: Session = Depends(get_db)):
    price_tag_crud.delete_update(db, price_tag_id, q, price_tag)
