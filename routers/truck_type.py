from typing import List
from fastapi import Depends, APIRouter, status
from data_base.database import get_db
from schemas import truck_type as truck_type_schema
from crud import truck_type as truck_type_crud
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/truck_type/", status_code=status.HTTP_201_CREATED)
def create_truck_type(truck_type: truck_type_schema.TruckTypeCreate, db: Session = Depends(get_db)):
    truck_type_crud.create(db, truck_type)


@router.get("/truck_type/{truck_type_id}",
            response_model=truck_type_schema.TruckTypeGet,
            status_code=status.HTTP_200_OK)
def get_truck_type(truck_type_id: int, db: Session = Depends(get_db)):
    return truck_type_crud.read(db, truck_type_id)


@router.get("/truck_type/", response_model=List[truck_type_schema.TruckTypeGet], status_code=status.HTTP_200_OK)
def get_all_truck_types(db: Session = Depends(get_db)):
    return truck_type_crud.read_all(db)
