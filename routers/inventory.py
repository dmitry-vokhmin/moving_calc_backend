from typing import List
from fastapi import Depends, APIRouter, status
from data_base.database import get_db
from schemas import inventory as inventory_schema
from crud import inventory as inventory_crud
from sqlalchemy.orm import Session
from security.security import get_user_id

router = APIRouter(tags=["Inventory"])


@router.post("/inventory/", status_code=status.HTTP_201_CREATED)
def create_inventory(inventory: inventory_schema.InventoryCreate,
                     db: Session = Depends(get_db),
                     user_id: int = Depends(get_user_id)):
    inventory_crud.create(db, inventory, user_id)


@router.get("/inventory/", response_model=List[inventory_schema.InventoryGet],
            status_code=status.HTTP_200_OK)
def get_all_inventory(room_collection_id: int = None,
                      inventory_collection_id: int = None,
                      db: Session = Depends(get_db),
                      user_id: int = Depends(get_user_id)):
    return inventory_crud.read_all_by_id(db, room_collection_id, inventory_collection_id, user_id)


@router.delete("/inventory/", status_code=status.HTTP_200_OK)
def delete_inventory(inventory_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_user_id)):
    inventory_crud.delete(db, inventory_id, user_id)


@router.put("/inventory/", status_code=status.HTTP_200_OK)
def update_inventory(inventory_id: int,
                     inventory: inventory_schema.InventoryBase,
                     db: Session = Depends(get_db),
                     user_id: int = Depends(get_user_id)):
    inventory_crud.update(db, inventory_id, inventory, user_id)
