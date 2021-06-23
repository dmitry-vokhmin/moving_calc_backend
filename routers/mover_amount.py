from typing import List
from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session
from data_base.database import get_db
from schemas import mover_amount as mover_amount_schema
from crud import mover_amount as mover_amount_crud
from security.security import get_user_id


router = APIRouter(tags=["Mover amount"])


@router.post("/mover_amount/", status_code=status.HTTP_201_CREATED)
def create_mover_amount(mover_amount: mover_amount_schema.MoverAmountCreate,
                        db: Session = Depends(get_db),
                        user_id=Depends(get_user_id)):
    mover_amount_crud.create(db, mover_amount, user_id)


@router.get("/mover_amount/",
            response_model=List[mover_amount_schema.MoverAmountGet],
            status_code=status.HTTP_200_OK)
def get_all_mover_amount(db: Session = Depends(get_db)):
    return mover_amount_crud.read_all(db)


@router.delete("/mover_amount/", status_code=status.HTTP_200_OK)
def delete_mover_amount(mover_amount_id: int, db: Session = Depends(get_db), user_id=Depends(get_user_id)):
    mover_amount_crud.delete(db, mover_amount_id, user_id)


@router.put("/mover_amount/", status_code=status.HTTP_200_OK)
def update_mover_amount(mover_amount_id: int,
                        mover_amount: mover_amount_schema.MoverAmountBase,
                        db: Session = Depends(get_db),
                        user_id=Depends(get_user_id)):
    mover_amount_crud.update(db, mover_amount_id, mover_amount, user_id)
