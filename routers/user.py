from typing import List
from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from data_base.database import get_db
from schemas import user as user_schema
from schemas import token as token_schema
from crud import user as user_crud
from security.security import verify_secret, create_access_token, get_user_id

router = APIRouter(tags=["User"])


@router.post("/registration/", status_code=status.HTTP_201_CREATED)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    user_crud.add_new_user(db, user)


@router.post("/registration/user/", status_code=status.HTTP_201_CREATED)
def add_new_user(user: user_schema.UserCreate, db: Session = Depends(get_db), user_id=Depends(get_user_id)):
    user_crud.add_new_user(db, user, user_id)


@router.get("/user/reset_pass/", status_code=status.HTTP_200_OK)
def get_one_time_pass(email: str = None, password: str = None, db: Session = Depends(get_db)):
    user_crud.one_time_pass(db, email, password)


@router.put("/user/reset_pass/", status_code=status.HTTP_200_OK)
def reset_password(user_data: user_schema.ResetPassword, db: Session = Depends(get_db)):
    user_crud.reset_password(db, user_data)


@router.get("/user/company/", response_model=List[user_schema.UserGet], status_code=status.HTTP_200_OK)
def get_all_company_users(db: Session = Depends(get_db), user_id=Depends(get_user_id)):
    return user_crud.company_user(db, user_id)


@router.get("/user/", response_model=user_schema.UserGet, status_code=status.HTTP_200_OK)
def read_user(db: Session = Depends(get_db), user_id=Depends(get_user_id)):
    return user_crud.read(db, user_id)


@router.put("/user/", response_model=user_schema.UserGet, status_code=status.HTTP_200_OK)
def update_user(user: user_schema.UserUpdate, db: Session = Depends(get_db), user_id=Depends(get_user_id)):
    return user_crud.user_update(db, user, user_id)


@router.delete("/user/", status_code=status.HTTP_200_OK)
def delete_user(user: user_schema.UserGet, db: Session = Depends(get_db), user_id=Depends(get_user_id)):
    user_crud.delete(db, user, user_id)


@router.post("/authorization/", response_model=token_schema.Token)
def auth(auth_form: user_schema.UserAuth, db: Session = Depends(get_db)):
    user_db = user_crud.read_by_user_email(db, auth_form)
    if user_db:
        is_pass_valid = verify_secret(auth_form.password.get_secret_value(), user_db.password)
        if is_pass_valid:
            encoded_jwt = create_access_token(user_db)
            return {"access_token": encoded_jwt, "token_type": "Bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email and/or password. Please try again",
        headers={"WWW-Authenticate": "Bearer"})
