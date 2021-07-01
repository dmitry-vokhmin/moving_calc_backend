from typing import List
from fastapi import Depends, APIRouter, status
from data_base.database import get_db
from schemas import move_size as move_size_schema
from crud import move_size as move_size_crud
from sqlalchemy.orm import Session
from security.security import get_user_id

router = APIRouter(tags=["Move size"])


@router.post("/move_size/", status_code=status.HTTP_201_CREATED)
def create_move_size(move_size: move_size_schema.MoveSizeCreate,
                     db: Session = Depends(get_db),
                     user_id=Depends(get_user_id)):
    move_size_crud.create(db, move_size, user_id)


@router.get("/move_size/", response_model=List[move_size_schema.MoveSizeGet], status_code=status.HTTP_200_OK)
def get_all_move_sizes(db: Session = Depends(get_db)):
    return move_size_crud.read_all(db)


@router.delete("/move_size/", status_code=status.HTTP_200_OK)
def delete_move_size(move_size_id: int, db: Session = Depends(get_db), user_id=Depends(get_user_id)):
    move_size_crud.delete(db, move_size_id, user_id)


@router.put("/move_size/", status_code=status.HTTP_200_OK)
def update_move_size(move_size_id: int,
                     move_size: move_size_schema.MoveSizeCreate,
                     db: Session = Depends(get_db),
                     user_id=Depends(get_user_id)):
    move_size_crud.update(db, move_size_id, move_size, user_id)
