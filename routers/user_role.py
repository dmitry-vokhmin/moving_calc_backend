from typing import List
from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session
from data_base.database import get_db
from schemas import user_role as user_role_schema
from crud import user_role as user_role_crud
from security.security import get_user_id

router = APIRouter(tags=["User Role"])


@router.post("/user_role/", status_code=status.HTTP_201_CREATED)
def create_user_role(user_role: user_role_schema.UserRoleCreate,
                     db: Session = Depends(get_db),
                     user_id=Depends(get_user_id)):
    user_role_crud.create(db, user_role, user_id)


@router.get("/user_role/", response_model=List[user_role_schema.UserRoleGet], status_code=status.HTTP_200_OK)
def get_all_user_roles_privilege(db: Session = Depends(get_db), user_id=Depends(get_user_id)):
    return user_role_crud.get_role_privilege(db, user_id)
