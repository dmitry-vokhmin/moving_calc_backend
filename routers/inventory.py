from typing import List
from fastapi import Depends, APIRouter, status
from data_base.database import get_db
from data_base import models
from schemas import inventory as inventory_schema
from crud import inventory as inventory_crud
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/inventory/", status_code=status.HTTP_201_CREATED)
def create_inventory(inventory: inventory_schema.InventoryCreate, db: Session = Depends(get_db)):
    inventory_crud.create(db, inventory)

@router.get("/inventory/", response_model=List[inventory_schema.InventoryGet], status_code=status.HTTP_200_OK)
def get_all_inventory(db: Session = Depends(get_db)):
    return inventory_crud.read_all(db)
