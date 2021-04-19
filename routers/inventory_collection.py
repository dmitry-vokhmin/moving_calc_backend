from typing import List
from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from data_base.database import get_db
from schemas import inventory_collection as inventory_collection_schema
from crud import inventory_collection as inventory_collection_crud
from security.security import get_current_user
from data_base.models import User

router = APIRouter(tags=["Inventory collection"])


@router.post("/inventory_collection/", status_code=status.HTTP_201_CREATED)
def create_inventory_collection(inventory_collection: inventory_collection_schema.InventoryCollectionCreate,
                                db: Session = Depends(get_db),
                                user: User = Depends(get_current_user)):
    if user.is_staff:
        inventory_collection_crud.create(db, inventory_collection)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post("/inventory_collection/{move_size_id}", status_code=status.HTTP_201_CREATED)
def update_many_to_many(move_size_id: int, inventory: List[int], db: Session = Depends(get_db)):
    inventory_collection_crud.update_many_to_many_inventory(db, move_size_id, inventory)


@router.get("/inventory_collection/{inventory_collection_id}",
            response_model=inventory_collection_schema.InventoryCollectionGet,
            status_code=status.HTTP_200_OK)
def get_inventory_collection(inventory_collection_id: int, db: Session = Depends(get_db)):
    return inventory_collection_crud.read(db, inventory_collection_id)


@router.get("/inventory_collection/",
            response_model=List[inventory_collection_schema.InventoryCollectionGet],
            status_code=status.HTTP_200_OK)
def get_all_inventory_collection(db: Session = Depends(get_db)):
    return inventory_collection_crud.read_all(db)
