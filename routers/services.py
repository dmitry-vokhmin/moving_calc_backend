from typing import List
from fastapi import Depends, APIRouter, status
from data_base.database import get_db
from schemas import services as services_schema
from crud import services as services_crud
from sqlalchemy.orm import Session
from security.security import get_user_id

router = APIRouter(tags=["Services"])


@router.post("/service/", status_code=status.HTTP_201_CREATED)
def create_services(services: services_schema.ServicesCreate,
                    db: Session = Depends(get_db),
                    user_id=Depends(get_user_id)):
    services_crud.create(db, services, user_id)


@router.get("/service/", response_model=List[services_schema.ServicesGet], status_code=status.HTTP_200_OK)
def get_all_services(db: Session = Depends(get_db)):
    return services_crud.read_all(db)


@router.delete("/service/", status_code=status.HTTP_200_OK)
def delete_service(service_id: int, db: Session = Depends(get_db), user_id=Depends(get_user_id)):
    services_crud.delete(db, service_id, user_id)


@router.put("/service/", status_code=status.HTTP_200_OK)
def update_service(service_id: int,
                   service: services_schema.ServicesBase,
                   db: Session = Depends(get_db),
                   user_id=Depends(get_user_id)):
    services_crud.update(db, service_id, service, user_id)
