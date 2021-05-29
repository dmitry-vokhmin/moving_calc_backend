from typing import List
from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from data_base.database import get_db
from data_base.models import User
from schemas import user_role as user_role_schema
from crud import user_role as user_role_crud
from security.security import get_current_user

router = APIRouter(tags=["User Role"])


@router.post("/user_role/", status_code=status.HTTP_201_CREATED)
def create_user_role(user_role: user_role_schema.UserRoleCreate,
                     db: Session = Depends(get_db),
                     user: User = Depends(get_current_user)):
    if user.is_staff:
        user_role_crud.create(db, user_role)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/user_role/{user_role_id}", response_model=user_role_schema.UserRoleGet, status_code=status.HTTP_200_OK)
def get_user_role(user_role_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.is_staff:
        return user_role_crud.read(db, user_role_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/user_role/", response_model=List[user_role_schema.UserRoleGet], status_code=status.HTTP_200_OK)
def get_all_user_roles_privilege(db: Session = Depends(get_db), user_id=Depends(get_current_user)):
    return user_role_crud.get_role_privilege(db, user_id)
