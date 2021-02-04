from typing import List
from fastapi import Depends, APIRouter, status
from data_base.database import get_db
from schemas import truck as truck_schema
from crud import truck as truck_crud
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/truck/", status_code=status.HTTP_201_CREATED)
def create_truck(truck: truck_schema.TruckCreate, db: Session = Depends(get_db)):
    truck_crud.create(db, truck)


@router.get("/truck/{truck_id}", response_model=truck_schema.TruckGet, status_code=status.HTTP_200_OK)
def get_truck(truck_id: int, db: Session = Depends(get_db)):
    return truck_crud.read(db, truck_id)


@router.get("/truck/", response_model=List[truck_schema.TruckGet], status_code=status.HTTP_200_OK)
def get_all_trucks(db: Session = Depends(get_db)):
    return truck_crud.read_all(db)
