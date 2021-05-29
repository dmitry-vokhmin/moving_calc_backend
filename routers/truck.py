from typing import List
from fastapi import Depends, APIRouter, status
from data_base.database import get_db
from schemas import truck as truck_schema
from crud import truck as truck_crud
from sqlalchemy.orm import Session
from security.security import get_current_user

router = APIRouter(tags=["Truck"])


@router.post("/truck/", status_code=status.HTTP_201_CREATED)
def create_truck(truck: truck_schema.TruckCreate,
                 db: Session = Depends(get_db),
                 user_id=Depends(get_current_user)):
    truck_crud.create(db, truck, user_id)


@router.get("/truck/{truck_id}", response_model=truck_schema.TruckGet, status_code=status.HTTP_200_OK)
def get_truck(truck_id: int, db: Session = Depends(get_db), user_id=Depends(get_current_user)):
    return truck_crud.read(db, truck_id, user_id)


@router.get("/truck/", response_model=List[truck_schema.TruckGet], status_code=status.HTTP_200_OK)
def get_all_trucks(db: Session = Depends(get_db), user_id=Depends(get_current_user)):
    return truck_crud.read_all(db, user_id)


@router.delete("/truck/", status_code=status.HTTP_200_OK)
def delete_truck(truck: truck_schema.TruckGet, db: Session = Depends(get_db), user_id=Depends(get_current_user)):
    truck_crud.delete(db, truck, user_id)


@router.put("/truck/", status_code=status.HTTP_200_OK)
def update_truck(truck: truck_schema.TruckUpdate,
                 db: Session = Depends(get_db),
                 user_id=Depends(get_current_user)):
    truck_crud.update(db, truck, user_id)
