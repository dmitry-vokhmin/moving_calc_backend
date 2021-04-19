from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from data_base.database import get_db
from schemas import user as user_schema
from schemas import token as token_schema
from crud import user as user_crud
from security.security import verify_secret, create_access_token, get_current_user
from data_base.models import User

router = APIRouter(tags=["User"])


@router.post("/registration/", response_model=user_schema.UserGet, status_code=status.HTTP_201_CREATED)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    return user_crud.create(db, user)


@router.get("/user/{user_id}", response_model=user_schema.UserGet, status_code=status.HTTP_200_OK)
def read_user(user_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.is_staff:
        return user_crud.read(db, user_id)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post("/authorization", response_model=token_schema.Token)
def auth(auth_form: user_schema.UserAuth, db: Session = Depends(get_db)):
    user_db = user_crud.read_by_user_name(db, auth_form)
    if user_db:
        is_pass_valid = verify_secret(auth_form.password.get_secret_value(), user_db.password)
        if is_pass_valid:
            encoded_jwt = create_access_token(user_db)
            return {"access_token": encoded_jwt, "token_type": "Bearer"}
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"})


@router.get("/users/me/", response_model=user_schema.UserGet)
async def read_users_me(user: User = Depends(get_current_user)):
    return user


def refresh():
    pass
