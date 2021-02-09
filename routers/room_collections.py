from typing import List
from fastapi import Depends, APIRouter, status
from data_base.database import get_db
from schemas import room_collection as room_collection_schema
from crud import room_collection as room_collection_crud
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/room_collection/", status_code=status.HTTP_201_CREATED)
def create_room_collection(room_collection: room_collection_schema.RoomCollectionsCreate,
                           db: Session = Depends(get_db)):
    room_collection_crud.create(db, room_collection)


@router.get("/room_collection/",
            response_model=List[room_collection_schema.RoomCollectionsCreate],
            status_code=status.HTTP_200_OK)
def get_all_room_collections(db: Session = Depends(get_db)):
    return room_collection_crud.read_all(db)
