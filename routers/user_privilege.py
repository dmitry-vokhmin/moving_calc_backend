from typing import List
from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session
from data_base.database import get_db
from schemas import user_privilege as user_privilege_schema
from crud import user_privilege as user_privilege_crud
from security.security import get_user_id


router = APIRouter(tags=["User Privilege"])


@router.post("/user_privilege/", status_code=status.HTTP_201_CREATED)
def create_user_privilege(user_privilege: user_privilege_schema.UserPrivilegeCreate,
                          db: Session = Depends(get_db),
                          user_id=Depends(get_user_id)):
    user_privilege_crud.create(db, user_privilege, user_id)


@router.get("/user_privilege/",
            response_model=List[user_privilege_schema.UserPrivilegeGet],
            status_code=status.HTTP_200_OK)
def get_all_user_privileges(db: Session = Depends(get_db), user_id=Depends(get_user_id)):
    return user_privilege_crud.read_user_privileges(db, user_id)
