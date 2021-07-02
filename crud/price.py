from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import price as mover_price_schema
from security.security import get_user, check_privilege


def create(db: Session, mover_price: mover_price_schema.MoverPriceCreate, company_id):
    mover_price_db = models.Price(**mover_price.dict(), company_id=company_id)
    db.add(mover_price_db)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def read_all(db: Session, user_id):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        query = db.query(models.Price)
    else:
        check_privilege(db, user_db, "configurations")
        query = db.query(models.Price).filter_by(company_id=user_db.company_id)
    return query.all()


def create_or_update(db: Session, mover_prices: mover_price_schema.MoverPriceUpdate, user_id):
    user_db = get_user(db, user_id)
    check_privilege(db, user_db, "configurations")
    for mover_price in mover_prices.__root__:
        try:
            create(db, mover_price, user_db.company_id)
        except HTTPException:
            db.query(models.Price).filter_by(mover_amount_id=mover_price.mover_amount_id,
                                             price_tag_id=mover_price.price_tag_id,
                                             company_id=user_db.company_id).update({"price": mover_price.price})
            try:
                db.commit()
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=400, detail=str(e))
