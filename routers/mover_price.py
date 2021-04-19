from typing import List
from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from data_base.database import get_db
from schemas import mover_price as mover_price_schema
from crud import mover_price as mover_price_crud
from security.security import get_current_user
from data_base.models import User

router = APIRouter(tags=["Mover Price"])


@router.post("/mover_price/", status_code=status.HTTP_201_CREATED)
def create_mover_price(mover_price: mover_price_schema.MoverPriceCreate,
                       db: Session = Depends(get_db),
                       user: User = Depends(get_current_user)):
    if user.is_staff:
        mover_price_crud.create(db, mover_price)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.get("/mover_price/{mover_price_id}", response_model=mover_price_schema.MoverPriceGet,
            status_code=status.HTTP_200_OK)
def get_mover_price(mover_price_id: int, db: Session = Depends(get_db)):
    return mover_price_crud.read(db, mover_price_id)


@router.get("/mover_price/", response_model=List[mover_price_schema.MoverPriceGet],
            status_code=status.HTTP_200_OK)
def get_all_mover_prices(db: Session = Depends(get_db)):
    return mover_price_crud.read_all(db)


@router.put("/mover_price/delete/{mover_price_id}", status_code=status.HTTP_200_OK)
def delete_mover_price(mover_price_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.is_staff:
        mover_price_crud.delete(db, mover_price_id)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.put("/mover_price/update/{mover_price_id}", status_code=status.HTTP_200_OK)
def update_mover_price(
        mover_price_id: int,
        mover_price: mover_price_schema.MoverPriceBase,
        db: Session = Depends(get_db)):
    mover_price_crud.update(db, mover_price_id, mover_price)
