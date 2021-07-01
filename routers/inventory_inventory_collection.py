from typing import List
from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session
from data_base.database import get_db
from schemas import inventory_inventory_collection as inventory_collection_schema
from crud import inventory_inventory_collection as inventory_collection_crud
from security.security import get_user_id

router = APIRouter(tags=["Inventory Inventory collection"])


@router.post("/inventory_inventory_collection/", status_code=status.HTTP_200_OK)
def update_inventory_collection(inventory_collection: inventory_collection_schema.InventoryInventoryCollectionCreate,
                                db: Session = Depends(get_db),
                                user_id: int = Depends(get_user_id)):
    return inventory_collection_crud.create(db, inventory_collection, user_id)


@router.get("/inventory_inventory_collection/",
            response_model=List[inventory_collection_schema.InventoryInventoryCollectionGet],
            status_code=status.HTTP_200_OK)
def get_inventory_collection(inventory_collection_id: int = None,
                             move_size_id: int = None,
                             db: Session = Depends(get_db),
                             user_id: int = Depends(get_user_id)):
    return inventory_collection_crud.read_all(db, inventory_collection_id, move_size_id, user_id)


@router.put("/inventory_inventory_collection/", status_code=status.HTTP_200_OK)
def update_inventory_collection(inventory_collection: inventory_collection_schema.InventoryInventoryCollectionUpdate,
                                db: Session = Depends(get_db),
                                user_id: int = Depends(get_user_id)):
    return inventory_collection_crud.bulk_update(db, inventory_collection, user_id)


@router.delete("/inventory_inventory_collection/", status_code=status.HTTP_200_OK)
def delete_inventory_collection(inventory_collection: inventory_collection_schema.InventoryInventoryCollectionDelete,
                                db: Session = Depends(get_db),
                                user_id: int = Depends(get_user_id)):
    inventory_collection_crud.delete_inventory(db, inventory_collection, user_id)