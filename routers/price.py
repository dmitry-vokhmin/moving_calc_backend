from typing import List
from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from data_base.database import get_db
from schemas import price as mover_price_schema
from crud import price as mover_price_crud
from security.security import get_user_id
from data_base.models import User

router = APIRouter(tags=["Mover Price"])


@router.post("/price/", status_code=status.HTTP_201_CREATED)
def create_mover_price(mover_price: mover_price_schema.MoverPriceCreate,
                       db: Session = Depends(get_db),
                       user: User = Depends(get_user_id)):
    mover_price_crud.create(db, mover_price, user.id)


@router.get("/price/{mover_price_id}", response_model=mover_price_schema.MoverPriceGet,
            status_code=status.HTTP_200_OK)
def get_mover_price(mover_price_id: int, db: Session = Depends(get_db), user: User = Depends(get_user_id)):
    return mover_price_crud.read(db, mover_price_id, user.id)


@router.get("/price/", response_model=List[mover_price_schema.MoverPriceGet],
            status_code=status.HTTP_200_OK)
def get_all_mover_prices(db: Session = Depends(get_db), user_id=Depends(get_user_id)):
    return mover_price_crud.read_all(db, user_id)


@router.delete("/price/", status_code=status.HTTP_200_OK)
def delete_mover_price(mover_price_id: int, db: Session = Depends(get_db), user: User = Depends(get_user_id)):
    mover_price_crud.delete(db, mover_price_id, user.id)


@router.put("/price/", status_code=status.HTTP_200_OK)
def update_mover_price(
        mover_price: mover_price_schema.MoverPriceUpdate,
        db: Session = Depends(get_db),
        user_id=Depends(get_user_id)):
    mover_price_crud.update(db, mover_price, user_id)
