from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session
from data_base.database import get_db
from schemas import inventory_order as inventory_order_schema
from crud import inventory_order as inventory_order_crud

router = APIRouter(tags=["Inventory Order"])


@router.post("/inventory_order/", status_code=status.HTTP_201_CREATED)
def post_inventory_order(inventory_order: inventory_order_schema.InventoryOrderCreate,
                         db: Session = Depends(get_db)):
    inventory_order_crud.create(db, inventory_order)
