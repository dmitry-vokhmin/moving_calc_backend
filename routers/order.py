from typing import List
from fastapi import Depends, APIRouter, status
from data_base.database import get_db
from schemas import order as order_schema
from crud import order as order_crud
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/order/", status_code=status.HTTP_201_CREATED)
def create_order(order: order_schema.OrderCreate, db: Session = Depends(get_db)):
    order_crud.create(db, order)

@router.get("/order/{order_id}", response_model=List[order_schema.OrderGet], status_code=status.HTTP_200_OK)
def get_order(order_id: int, db: Session = Depends(get_db)):
    return order_crud.read(db, order_id)
