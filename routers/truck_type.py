from typing import List
from fastapi import Depends, APIRouter, status
from data_base.database import get_db
from schemas import truck_type as truck_type_schema
from crud import truck_type as truck_type_crud
from sqlalchemy.orm import Session
from security.security import get_current_user
from data_base.models import User

router = APIRouter(tags=["Truck type"])


@router.post("/truck_type/", status_code=status.HTTP_201_CREATED)
def create_truck_type(truck_type: truck_type_schema.TruckTypeCreate,
                      db: Session = Depends(get_db),
                      user: User = Depends(get_current_user)):
    truck_type_crud.create(db, truck_type, user.id)


@router.get("/truck_type/{truck_type_id}",
            response_model=truck_type_schema.TruckTypeGet,
            status_code=status.HTTP_200_OK)
def get_truck_type(truck_type_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return truck_type_crud.read(db, truck_type_id, user.id)


@router.get("/truck_type/", response_model=List[truck_type_schema.TruckTypeGet], status_code=status.HTTP_200_OK)
def get_all_truck_types(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return truck_type_crud.read_all(db, user.id)


@router.put("/truck_type/delete/{truck_type_id}", status_code=status.HTTP_200_OK)
def delete_truck_type(truck_type_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    truck_type_crud.delete(db, truck_type_id, user.id)


@router.put("/truck_type/update/{truck_type_id}", status_code=status.HTTP_200_OK)
def update_truck_type(truck_type_id: int,
                      truck_type: truck_type_schema.TruckTypeBase,
                      db: Session = Depends(get_db),
                      user: User = Depends(get_current_user)):
    truck_type_crud.update(db, truck_type_id, truck_type, user.id)
