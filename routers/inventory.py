from typing import List
from fastapi import Depends, APIRouter, status
from data_base.database import get_db
from data_base import models
from schemas import inventory as inventory_schema
from crud import inventory as inventory_crud
from sqlalchemy.orm import Session

router = APIRouter(tags=["Inventory"])


@router.post("/inventory/", status_code=status.HTTP_201_CREATED)
def create_inventory(inventory: inventory_schema.InventoryCreate, db: Session = Depends(get_db)):
    inventory_crud.create(db, inventory)


@router.get("/inventory/{inventory_id}", response_model=inventory_schema.InventoryGet, status_code=status.HTTP_200_OK)
def get_inventory(inventory_id: int, db: Session = Depends(get_db)):
    return inventory_crud.read(db, inventory_id)


@router.get("/inventory/all/{room_name}", response_model=List[inventory_schema.InventoryGet],
            status_code=status.HTTP_200_OK)
def get_all_inventory(room_name: str, db: Session = Depends(get_db)):
    return inventory_crud.read_all(db, room_name)
