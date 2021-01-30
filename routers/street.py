from typing import List
from fastapi import Depends, APIRouter, status
from data_base.database import get_db
from data_base import models
from schemas import street as street_schema
from crud import street as street_crud
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/street/", status_code=status.HTTP_201_CREATED)
def create_street(street: street_schema.StreetCreate, db: Session = Depends(get_db)):
    street_crud.create(db, street)

@router.get("/street/{street_id}", response_model=List[street_schema.StreetGet], status_code=status.HTTP_200_OK)
def get_street(street_id: int, db: Session = Depends(get_db)):
    return street_crud.read(db, street_id)

@router.get("/street/", response_model=List[street_schema.StreetGet], status_code=status.HTTP_200_OK)
def get_all_street(db: Session = Depends(get_db)):
    return street_crud.read_all(db)
