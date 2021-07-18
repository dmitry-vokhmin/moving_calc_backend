from fastapi import Depends, APIRouter, status
from data_base.database import get_db
from schemas import address as address_schema
from crud import address as address_crud
from sqlalchemy.orm import Session

router = APIRouter(tags=["Address"])


@router.post("/address/", response_model=address_schema.AddressGet, status_code=status.HTTP_201_CREATED)
def create_address(address: address_schema.AddressCreate, db: Session = Depends(get_db)):
    return address_crud.get_or_create(db, address)


@router.get("/address/", response_model=address_schema.AddressGet, status_code=status.HTTP_200_OK)
def get_address(address_id: int, db: Session = Depends(get_db)):
    return address_crud.read(db, address_id)
