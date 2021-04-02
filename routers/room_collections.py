from typing import List
from fastapi import Depends, APIRouter, status
from data_base.database import get_db
from schemas import room_collection as room_collection_schema
from crud import room_collection as room_collection_crud
from sqlalchemy.orm import Session

router = APIRouter(tags=["Room collection"])


@router.post("/room_collection/", status_code=status.HTTP_201_CREATED)
def create_room_collection(room_collection: room_collection_schema.RoomCollectionsCreate,
                           db: Session = Depends(get_db)):
    room_collection_crud.create(db, room_collection)


@router.post("/room_collection/{room_id}")
def create_many_to_many(room_id: int, inventory: List[str], db: Session = Depends(get_db)):
    room_collection_crud.create_many_to_many_inventory(db, room_id, inventory)


@router.get("/room_collection/{room_collection_id}",
            response_model=room_collection_schema.RoomCollectionsGet,
            status_code=status.HTTP_200_OK)
def get_room_collection(room_collection_id: int, db: Session = Depends(get_db)):
    return room_collection_crud.read(db, room_collection_id)


@router.get("/room_collection/",
            response_model=List[room_collection_schema.RoomCollectionsGet],
            status_code=status.HTTP_200_OK)
def get_all_room_collections(db: Session = Depends(get_db)):
    return room_collection_crud.read_all(db)


@router.put("/room_collection/{room_id}", status_code=status.HTTP_200_OK)
def delete_room_collection_inventory(room_id: int, inventory: list, db: Session = Depends(get_db)):
    room_collection_crud.delete(db, room_id, inventory)