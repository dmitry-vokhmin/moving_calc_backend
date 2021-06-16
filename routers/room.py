from typing import List
from fastapi import Depends, APIRouter, status
from data_base.database import get_db
from schemas import room as room_schema
from crud import room as room_crud
from sqlalchemy.orm import Session
from security.security import get_user_id
from data_base.models import User

router = APIRouter(tags=["Room"])


@router.post("/room/", status_code=status.HTTP_201_CREATED)
def create_room(room: room_schema.RoomCreate,
                db: Session = Depends(get_db),
                user_id: User = Depends(get_user_id)):
    room_crud.create(db, room)


@router.get("/room/{room_id}", response_model=room_schema.RoomGet, status_code=status.HTTP_200_OK)
def get_room(room_id: int, db: Session = Depends(get_db), user_id: User = Depends(get_user_id)):
    return room_crud.read(db, room_id, user_id)


@router.get("/room/", response_model=List[room_schema.RoomGet], status_code=status.HTTP_200_OK)
def get_all_rooms(db: Session = Depends(get_db)):
    return room_crud.read_all(db)
