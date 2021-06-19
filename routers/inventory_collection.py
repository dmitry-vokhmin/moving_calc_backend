from typing import List
from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from data_base.database import get_db
from schemas import inventory_collection as inventory_collection_schema
from crud import inventory_collection as inventory_collection_crud
from security.security import get_user_id
from data_base.models import User

router = APIRouter(tags=["Inventory collection"])


@router.post("/inventory_collection/", status_code=status.HTTP_201_CREATED)
def create_personal_inventory_collection(
        inventory_collection: inventory_collection_schema.InventoryCollectionCreate,
        db: Session = Depends(get_db),
        user_id: int = Depends(get_user_id)):
    inventory_collection_crud.create_public(db, inventory_collection, user_id)


@router.get("/inventory_collection/{inventory_collection_id}",
            response_model=inventory_collection_schema.InventoryCollectionGet,
            status_code=status.HTTP_200_OK)
def get_inventory_collection(inventory_collection_id: int,
                             db: Session = Depends(get_db),
                             user_id: int = Depends(get_user_id)):
    return inventory_collection_crud.read(db, inventory_collection_id, user_id)


@router.get("/inventory_collection/",
            response_model=List[inventory_collection_schema.InventoryCollectionGet],
            status_code=status.HTTP_200_OK)
def get_all_inventory_collection(db: Session = Depends(get_db), user_id: int = Depends(get_user_id)):
    return inventory_collection_crud.read_all(db, user_id)


@router.delete("/inventory_collection/", status_code=status.HTTP_200_OK)
def reset_inventory_collection(inventory_collection_id: int,
                               db: Session = Depends(get_db),
                               user_id: int = Depends(get_user_id)):
    inventory_collection_crud.reset_inventory(db, inventory_collection_id, user_id)


@router.put("/inventory_collection/", status_code=status.HTTP_200_OK)
def update_inventory_collection(inventory_collection_id: int,
                                inventory_collection: inventory_collection_schema.InventoryCollectionCreate,
                                db: Session = Depends(get_db),
                                user_id: int = Depends(get_user_id)):
    inventory_collection_crud.update(db, inventory_collection_id, inventory_collection, user_id)

