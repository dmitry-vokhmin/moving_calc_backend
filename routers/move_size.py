from typing import List
from fastapi import Depends, APIRouter, status
from data_base.database import get_db
from schemas import move_size as move_size_schema
from crud import move_size as move_size_crud
from sqlalchemy.orm import Session

router = APIRouter(tags=["Move size"])


@router.post("/move_size/", status_code=status.HTTP_201_CREATED)
def create_move_size(move_size: move_size_schema.MoveSizeCreate, db: Session = Depends(get_db)):
    move_size_crud.create(db, move_size)


@router.get("/move_size/{move_size_id}", response_model=move_size_schema.MoveSizeGet, status_code=status.HTTP_200_OK)
def get_move_size(move_size_id: int, q: str = None, db: Session = Depends(get_db)):
    return move_size_crud.read(db, move_size_id, q)


@router.get("/move_size/", response_model=List[move_size_schema.MoveSizeGet], status_code=status.HTTP_200_OK)
def get_all_move_sizes(db: Session = Depends(get_db)):
    return move_size_crud.read_all(db)
