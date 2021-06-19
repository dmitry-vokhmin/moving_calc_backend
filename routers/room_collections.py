from typing import List
from fastapi import Depends, APIRouter, status
from data_base.database import get_db
from schemas import room_collection as room_collection_schema
from crud import room_collection as room_collection_crud
from sqlalchemy.orm import Session
from security.security import get_user_id
from data_base.models import User

router = APIRouter(tags=["Room collection"])


@router.post("/room_collection/", status_code=status.HTTP_201_CREATED)
def create_room_collection(room_collection: room_collection_schema.RoomCollectionsCreate,
                           db: Session = Depends(get_db),
                           user_id: int = Depends(get_user_id)):
    room_collection_crud.create(db, room_collection, user_id)


@router.get("/room_collection/",
            response_model=List[room_collection_schema.RoomCollectionsGet],
            status_code=status.HTTP_200_OK)
def get_all_room_collections(db: Session = Depends(get_db), user_id: int = Depends(get_user_id)):
    return room_collection_crud.read_all(db, user_id)


@router.delete("/room_collection/", status_code=status.HTTP_200_OK)
def delete_inventory(inventory_id: int, db: Session = Depends(get_db), user_id: User = Depends(get_user_id)):
    return room_collection_crud.delete_inventory(db, inventory_id, user_id)


@router.put("/room_collection/inventory", status_code=status.HTTP_200_OK)
def update_inventory(room_collection_id: int,
                     inventory: list,
                     db: Session = Depends(get_db),
                     user_id: User = Depends(get_user_id)):
    return room_collection_crud.update_many_to_many_inventory(db, room_collection_id, inventory, user_id)
