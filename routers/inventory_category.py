from typing import List
from fastapi import Depends, APIRouter, status
from data_base.database import get_db
from schemas import inventory_category as inventory_category_schema
from crud import inventory_category as inventory_category_crud
from sqlalchemy.orm import Session
from security.security import get_user_id

router = APIRouter(tags=["Inventory Category"])


@router.post("/inventory_category/", status_code=status.HTTP_201_CREATED)
def create_inventory_category(inventory_category: inventory_category_schema.InventoryCategoryCreate,
                              db: Session = Depends(get_db),
                              user_id: int = Depends(get_user_id)):
    inventory_category_crud.create(db, inventory_category, user_id)


@router.get("/inventory_category/",
            response_model=List[inventory_category_schema.InventoryCategoryGet], status_code=status.HTTP_200_OK)
def get_all_inventory_categories(room_id: int = None, db: Session = Depends(get_db)):
    return inventory_category_crud.read_all(db, room_id)


@router.delete("/inventory_category/", status_code=status.HTTP_201_CREATED)
def delete_inventory_category(inventory_category_id: int,
                              db: Session = Depends(get_db),
                              user_id: int = Depends(get_user_id)):
    inventory_category_crud.delete(db, inventory_category_id, user_id)


@router.put("/inventory_category/", status_code=status.HTTP_201_CREATED)
def update_inventory_category(inventory_category_id: int,
                              inventory_category: inventory_category_schema.InventoryCategoryCreate,
                              db: Session = Depends(get_db),
                              user_id: int = Depends(get_user_id)):
    inventory_category_crud.update(db, inventory_category_id, inventory_category, user_id)
