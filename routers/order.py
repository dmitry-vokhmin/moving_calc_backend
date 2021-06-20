from typing import List
from fastapi import Depends, APIRouter, status
from data_base.database import get_db
from schemas import order as order_schema
from crud import order as order_crud
from sqlalchemy.orm import Session
from security.security import get_user_id

router = APIRouter(tags=["Order"])


@router.post("/order/", response_model=order_schema.OrderGet, status_code=status.HTTP_201_CREATED)
def create_order(order: order_schema.OrderCreate, db: Session = Depends(get_db)):
    return order_crud.create(db, order)


@router.get("/order/{order_id}", response_model=order_schema.OrderGet, status_code=status.HTTP_200_OK)
def get_order(order_id: int, db: Session = Depends(get_db), user_id=Depends(get_user_id)):
    return order_crud.read(db, order_id, user_id)


@router.get("/order/", response_model=List[order_schema.OrderGet], status_code=status.HTTP_200_OK)
def get_all_orders(db: Session = Depends(get_db), user_id=Depends(get_user_id)):
    return order_crud.read_all(db, user_id)
