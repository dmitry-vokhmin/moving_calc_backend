from typing import List
from fastapi import Depends, APIRouter, status, HTTPException
from data_base.database import get_db
from schemas import services as services_schema
from crud import services as services_crud
from sqlalchemy.orm import Session
from security.security import get_user_id
from data_base.models import User

router = APIRouter(tags=["Services"])


@router.post("/service/", status_code=status.HTTP_201_CREATED)
def create_services(services: services_schema.ServicesCreate,
                    db: Session = Depends(get_db),
                    user: User = Depends(get_user_id)):
    if user.is_staff:
        services_crud.create(db, services)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/service/{services_id}", response_model=services_schema.ServicesGet, status_code=status.HTTP_200_OK)
def get_services(services_id: int, q: str = None, db: Session = Depends(get_db)):
    return services_crud.read(db, services_id, q)


@router.get("/service/", response_model=List[services_schema.ServicesGet], status_code=status.HTTP_200_OK)
def get_all_services(db: Session = Depends(get_db)):
    return services_crud.read_all(db)


@router.put("/service/delete/{service_id}", status_code=status.HTTP_200_OK)
def delete_service(service_id: int, db: Session = Depends(get_db), user: User = Depends(get_user_id)):
    if user.is_staff:
        services_crud.delete(db, service_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.put("/service/update/{service_id}", status_code=status.HTTP_200_OK)
def update_service(service_id: int,
                   service: services_schema.ServicesBase,
                   db: Session = Depends(get_db),
                   user: User = Depends(get_user_id)):
    if user.is_staff:
        services_crud.update(db, service_id, service)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
