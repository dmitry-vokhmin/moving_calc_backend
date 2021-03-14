from typing import List
from fastapi import Depends, APIRouter, status
from data_base.database import get_db
from data_base import models
from schemas import floor_collection as floor_collection_schema
from crud import floor_collection as floor_collection_crud
from sqlalchemy.orm import Session

router = APIRouter(tags=["Floor collection"])


@router.post("/floor_collection/", status_code=status.HTTP_201_CREATED)
def create_floor_collection(floor_collection: floor_collection_schema.FloorCollectionCreate,
                            db: Session = Depends(get_db)):
    floor_collection_crud.create(db, floor_collection)


@router.get("/floor_collection/{floor_collection_id}",
            response_model=floor_collection_schema.FloorCollectionGet,
            status_code=status.HTTP_200_OK)
def get_floor_collection(floor_collection_id: int, q: str, db: Session = Depends(get_db)):
    return floor_collection_crud.read(db, floor_collection_id, q)


@router.get("/floor_collection/",
            response_model=List[floor_collection_schema.FloorCollectionGet],
            status_code=status.HTTP_200_OK)
def get_all_floor_collection(db: Session = Depends(get_db)):
    return floor_collection_crud.read_all(db)
