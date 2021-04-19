from typing import List
from fastapi import Depends, APIRouter, status, HTTPException
from data_base.database import get_db
from schemas import inventory as inventory_schema
from crud import inventory as inventory_crud
from sqlalchemy.orm import Session
from security.security import get_current_user
from data_base.models import User

router = APIRouter(tags=["Inventory"])


@router.post("/inventory/", status_code=status.HTTP_201_CREATED)
def create_inventory(inventory: inventory_schema.InventoryCreate,
                     db: Session = Depends(get_db),
                     user: User = Depends(get_current_user)):
    if user.is_staff:
        inventory_crud.create(db, inventory)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.get("/inventory/{inventory_id}", response_model=inventory_schema.InventoryGet, status_code=status.HTTP_200_OK)
def get_inventory(inventory_id: int, db: Session = Depends(get_db)):
    return inventory_crud.read(db, inventory_id)


@router.get("/inventory/all/{room_name}", response_model=List[inventory_schema.InventoryGet],
            status_code=status.HTTP_200_OK)
def get_all_inventory(room_name: str, db: Session = Depends(get_db)):
    return inventory_crud.read_all(db, room_name)
