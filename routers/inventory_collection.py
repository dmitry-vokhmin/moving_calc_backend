from typing import List
from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session
from data_base.database import get_db
from schemas import inventory_collection as inventory_collection_schema
from crud import inventory_collection as inventory_collection_crud

router = APIRouter(tags=["Inventory collection"])


@router.post("/inventory_collection/", status_code=status.HTTP_201_CREATED)
def create_inventory_collection(inventory_collection: inventory_collection_schema.InventoryCollectionCreate,
                                db: Session = Depends(get_db)):
    inventory_collection_crud.create(db, inventory_collection)


@router.post("/inventory_collection/{move_size_id}")
def create_many_to_many(room_id: int, inventory_list: List[str], db: Session = Depends(get_db)):
    inventory_collection_crud.create_many_to_many_inventory(db, room_id, inventory_list)


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


@router.put("/inventory_collection/{inventory_collection_id}", status_code=status.HTTP_200_OK)
def delete_inventory_collection_inventory(inventory_collection_id: int, inventory_list: list,
                                          db: Session = Depends(get_db)):
    inventory_collection_crud.delete(db, inventory_collection_id, inventory_list)
