from typing import List
from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from data_base.database import get_db
from schemas import price_tag_name as price_tag_name_schema
from crud import price_tag_name as price_tag_name_crud
from security.security import get_current_user
from data_base.models import User


router = APIRouter(tags=["Price tag name"])


@router.post("/price_tag_name/", status_code=status.HTTP_201_CREATED)
def create_price_tag(price_tag_name: price_tag_name_schema.PriceTagNameCreate,
                     db: Session = Depends(get_db),
                     user: User = Depends(get_current_user)):
    if user.is_staff:
        price_tag_name_crud.create(db, price_tag_name)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/price_tag_name/{price_tag_name_id}",
            response_model=price_tag_name_schema.PriceTagNameGet,
            status_code=status.HTTP_200_OK)
def get_price_tag_name(price_tag_name_id: int, db: Session = Depends(get_db)):
    return price_tag_name_crud.read(db, price_tag_name_id)


@router.get("/price_tag_name/",
            response_model=List[price_tag_name_schema.PriceTagNameGet],
            status_code=status.HTTP_200_OK)
def get_all_price_tag_name(db: Session = Depends(get_db)):
    return price_tag_name_crud.read_all(db)


@router.put("/price_tag_name/delete/{price_tag_name_id}", status_code=status.HTTP_200_OK)
def delete_price_tag_name(price_tag_name_id: int,
                          db: Session = Depends(get_db),
                          user: User = Depends(get_current_user)):
    if user.is_staff:
        price_tag_name_crud.delete(db, price_tag_name_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.put("/price_tag_name/update/{price_tag_name_id}", status_code=status.HTTP_200_OK)
def update_price_tag_name(price_tag_name_id: int,
                          price_tag_name: price_tag_name_schema.PriceTagNameBase,
                          db: Session = Depends(get_db),
                          user: User = Depends(get_current_user)):
    if user.is_staff:
        price_tag_name_crud.update(db, price_tag_name_id, price_tag_name)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
