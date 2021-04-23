from typing import List
from fastapi import Depends, APIRouter, status, HTTPException
from data_base.database import get_db
from schemas import room_collection as room_collection_schema
from crud import room_collection as room_collection_crud
from sqlalchemy.orm import Session
from security.security import get_current_user
from data_base.models import User

router = APIRouter(tags=["Room collection"])


@router.post("/room_collection/", status_code=status.HTTP_201_CREATED)
def create_room_collection(room_collection: room_collection_schema.RoomCollectionsCreate,
                           db: Session = Depends(get_db),
                           user: User = Depends(get_current_user)):
    if user.is_staff:
        room_collection_crud.create(db, room_collection)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/room_collection/{room_id}")
def update_many_to_many(room_id: int, inventory: List[int],
                        db: Session = Depends(get_db),
                        user: User = Depends(get_current_user)):
    if user.is_staff:
        room_collection_crud.update_many_to_many_inventory(db, room_id, inventory)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


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



