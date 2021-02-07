from typing import List
from fastapi import Depends, APIRouter, status
from data_base.database import get_db
from data_base import models
from schemas import address as address_schema
from crud import address as address_crud
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/address/", response_model=address_schema.AddressGet, status_code=status.HTTP_201_CREATED)
def create_address(address: address_schema.AddressCreate, db: Session = Depends(get_db)):
    return address_crud.create(db, address)

@router.get("/address/{address_id}", response_model=address_schema.AddressGet, status_code=status.HTTP_200_OK)
def get_address(address_id: int, db: Session = Depends(get_db)):
    return address_crud.read(db, address_id)

@router.get("/address/", response_model=List[address_schema.AddressGet], status_code=status.HTTP_200_OK)
def get_all_addresses(db: Session = Depends(get_db)):
    return address_crud.read_all(db)
