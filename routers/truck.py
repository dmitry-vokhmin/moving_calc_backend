from typing import List
from fastapi import Depends, APIRouter, status
from data_base.database import get_db
from schemas import truck as truck_schema
from crud import truck as truck_crud
from sqlalchemy.orm import Session
from security.security import get_current_user
from data_base.models import User

router = APIRouter(tags=["Truck"])


@router.post("/truck/", status_code=status.HTTP_201_CREATED)
def create_truck(truck: truck_schema.TruckCreate,
                 db: Session = Depends(get_db),
                 user: User = Depends(get_current_user)):
    truck_crud.create(db, truck, user.id)


@router.get("/truck/{truck_id}", response_model=truck_schema.TruckGet, status_code=status.HTTP_200_OK)
def get_truck(truck_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return truck_crud.read(db, truck_id, user.id)


@router.get("/truck/", response_model=List[truck_schema.TruckGet], status_code=status.HTTP_200_OK)
def get_all_trucks(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return truck_crud.read_all(db, user.id)


@router.put("/truck/delete/{truck_id}", status_code=status.HTTP_200_OK)
def delete_truck(truck_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    truck_crud.delete(db, truck_id, user.id)


@router.put("/truck/update/{truck_id}", status_code=status.HTTP_200_OK)
def update_truck(truck_id: int, truck: truck_schema.TruckCreate,
                 db: Session = Depends(get_db),
                 user: User = Depends(get_current_user)):
    truck_crud.update(db, truck_id, truck, user.id)
