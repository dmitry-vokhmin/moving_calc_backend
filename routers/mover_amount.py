from typing import List
from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from data_base.database import get_db
from schemas import mover_amount as mover_amount_schema
from crud import mover_amount as mover_amount_crud
from security.security import get_user_id
from data_base.models import User


router = APIRouter(tags=["Mover amount"])


@router.post("/mover_amount/", status_code=status.HTTP_201_CREATED)
def create_mover_amount(mover_amount: mover_amount_schema.MoverAmountCreate,
                        db: Session = Depends(get_db),
                        user: User = Depends(get_user_id)):
    if user.is_staff:
        mover_amount_crud.create(db, mover_amount)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/mover_amount/{mover_amount_id}",
            response_model=mover_amount_schema.MoverAmountGet,
            status_code=status.HTTP_200_OK)
def get_mover_amount(mover_amount_id: int, db: Session = Depends(get_db)):
    return mover_amount_crud.read(db, mover_amount_id)


@router.get("/mover_amount/",
            response_model=List[mover_amount_schema.MoverAmountGet],
            status_code=status.HTTP_200_OK)
def get_all_mover_amount(db: Session = Depends(get_db)):
    return mover_amount_crud.read_all(db)


@router.delete("/mover_amount/", status_code=status.HTTP_200_OK)
def delete_mover_amount(mover_amount_id: int, db: Session = Depends(get_db), user: User = Depends(get_user_id)):
    if user.is_staff:
        mover_amount_crud.delete(db, mover_amount_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.put("/mover_amount/", status_code=status.HTTP_200_OK)
def update_mover_amount(mover_amount_id: int,
                        mover_amount: mover_amount_schema.MoverAmountBase,
                        db: Session = Depends(get_db),
                        user: User = Depends(get_user_id)):
    if user.is_staff:
        mover_amount_crud.update(db, mover_amount_id, mover_amount)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
