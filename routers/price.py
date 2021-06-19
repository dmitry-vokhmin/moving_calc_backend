from typing import List
from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session
from data_base.database import get_db
from schemas import price as mover_price_schema
from crud import price as mover_price_crud
from security.security import get_user_id

router = APIRouter(tags=["Mover Price"])


@router.get("/price/", response_model=List[mover_price_schema.MoverPriceGet],
            status_code=status.HTTP_200_OK)
def get_all_mover_prices(db: Session = Depends(get_db), user_id=Depends(get_user_id)):
    return mover_price_crud.read_all(db, user_id)


@router.put("/price/", status_code=status.HTTP_200_OK)
def update_mover_price(
        mover_price: mover_price_schema.MoverPriceUpdate,
        db: Session = Depends(get_db),
        user_id=Depends(get_user_id)):
    mover_price_crud.create_or_update(db, mover_price, user_id)
