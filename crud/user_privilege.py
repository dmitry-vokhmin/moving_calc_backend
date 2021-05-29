from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import user_privilege as user_privilege_schema
from security.security import get_user


def create(db: Session, user_privilege: user_privilege_schema.UserPrivilegeCreate):
    user_privilege_db = models.UserPrivilege(**user_privilege.dict())
    db.add(user_privilege_db)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e.orig))


def read(db: Session, user_privilege_id: int):
    user_privilege_db = db.query(models.UserPrivilege).filter_by(id=user_privilege_id).first()
    return user_privilege_db


def read_all(db: Session):
    user_privilege_db = db.query(models.UserPrivilege).all()
    return user_privilege_db


def read_user_privileges(db: Session, user_id):
    user_db = get_user(db, user_id)
    user_privilege_db = db.query(models.UserPrivilege).filter(
        models.UserPrivilege.user_role.any(id=user_db.user_role_id)
    )
    return user_privilege_db.all()
