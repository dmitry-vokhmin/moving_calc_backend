from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import user as user_schema
from security.security import get_secret_hash, verify_secret, get_user
from crud.user_role import check_user_role_privilege


def valid_password(user, user_db):
    if user.old_password and user.password:
        if verify_secret(user.old_password.get_secret_value(), user_db.password):
            return True
        else:
            raise HTTPException(status_code=400, detail="Old password does not match")


def allowed_company_and_role(user, user_db, role_privileges):
    if user_db.company_id == user.company_id and user.user_role_id in {role.id for role in role_privileges}:
        return True
    raise HTTPException(status_code=400, detail="Don`t have permissions")


def get_user_role_privilege(db, user_id):
    user_db = get_user(db, user_id)
    role_privileges = check_user_role_privilege(db, user_db)
    return user_db, role_privileges


# def create(db: Session, user: user_schema.UserCreate):
#     user_db = models.User(
#         fullname=user.fullname,
#         email=user.email,
#         password=get_secret_hash(user.password.get_secret_value()),
#         company_id=user.company_id,
#         user_role_id=user.user_role_id
#     )
#     db.add(user_db)
#     try:
#         db.commit()
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=400, detail=str(e.orig))
#     return user_db


def add_new_user(db: Session, user: user_schema.UserCreate, user_id: int = None):
    if user_id:
        current_user, role_privileges = get_user_role_privilege(db, user_id)
        allowed_company_and_role(user, current_user, role_privileges)
    user_db = models.User(
        fullname=user.fullname,
        email=user.email,
        password=get_secret_hash(user.password.get_secret_value()),
        company_id=user.company_id,
        user_role_id=user.user_role_id
    )
    db.add(user_db)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e.orig))
    return user_db


def user_update(db: Session, user: user_schema.UserUpdate, user_id: int):
    user_db, role_privileges = get_user_role_privilege(db, user_id)
    if (user.user_role_id in {role.id for role in role_privileges} or user.id == user_db.id) \
            and user_db.company_id == user.company_id:
        if valid_password(user, user_db):
            user.password = get_secret_hash(user.password.get_secret_value())
        db.query(models.User).filter_by(id=user.id).update({**user.dict(exclude={"old_password"}, exclude_unset=True)})
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e.orig))
        return db.query(models.User).filter_by(id=user.id).first()
    raise HTTPException(status_code=400, detail="Don`t have permissions")


def read(db: Session, main_user_id: int, user_id: int = None):
    user_db = get_user(db, main_user_id)
    if user_id:
        staff_db = get_user(db, user_id)
        role_privileges = check_user_role_privilege(db, user_db)
        if allowed_company_and_role(staff_db, user_db, role_privileges):
            return staff_db
    if not user_db.user_role_id:
        raise HTTPException(status_code=400, detail="Account is not ready")
    return user_db


def delete(db: Session, user: user_schema.UserGet, user_id: int):
    user_db, role_privileges = get_user_role_privilege(db, user_id)
    if allowed_company_and_role(user, user_db, role_privileges):
        db.query(models.User).filter_by(id=user.id).delete()
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e.orig))


def company_user(db: Session, user_id: int):
    user_db, role_privileges = get_user_role_privilege(db, user_id)
    if role_privileges:
        user_db = db.query(models.User).filter_by(company_id=user_db.company_id)
        return user_db.all()
    else:
        raise HTTPException(status_code=400, detail="Not admin of the company")


def read_by_user_email(db: Session, user: user_schema.UserAuth):
    user_db = db.query(models.User).filter_by(email=user.email).first()
    return user_db
