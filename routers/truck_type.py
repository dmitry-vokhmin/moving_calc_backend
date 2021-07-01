from typing import List
from fastapi import Depends, APIRouter, status
from data_base.database import get_db
from schemas import truck_type as truck_type_schema
from crud import truck_type as truck_type_crud
from sqlalchemy.orm import Session
from security.security import get_user_id

router = APIRouter(tags=["Truck type"])


@router.post("/truck_type/", status_code=status.HTTP_201_CREATED)
def create_truck_type(truck_type: truck_type_schema.TruckTypeCreate,
                      db: Session = Depends(get_db),
                      user_id=Depends(get_user_id)):
    truck_type_crud.create(db, truck_type, user_id)


@router.get("/truck_type/", response_model=List[truck_type_schema.TruckTypeGet], status_code=status.HTTP_200_OK)
def get_all_truck_types(user_id=Depends(get_user_id), db: Session = Depends(get_db)):
    return truck_type_crud.read_all(db, user_id)


@router.delete("/truck_type/", status_code=status.HTTP_200_OK)
def delete_truck_type(truck_type: truck_type_schema.TruckTypeGet,
                      db: Session = Depends(get_db),
                      user_id=Depends(get_user_id)):
    truck_type_crud.delete(db, truck_type, user_id)


@router.put("/truck_type/", status_code=status.HTTP_200_OK)
def update_truck_type(truck_type: truck_type_schema.TruckTypeUpdate,
                      db: Session = Depends(get_db),
                      user_id=Depends(get_user_id)):
    truck_type_crud.update(db, truck_type, user_id)
