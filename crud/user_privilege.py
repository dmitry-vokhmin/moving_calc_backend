from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException, status
from schemas import user_privilege as user_privilege_schema
from security.security import get_user


def create(db: Session, user_privilege: user_privilege_schema.UserPrivilegeCreate, user_id):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        user_privilege_db = models.UserPrivilege(**user_privilege.dict())
        db.add(user_privilege_db)
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e.orig))
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def read_user_privileges(db: Session, user_id):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        user_privilege_db = db.query(models.UserPrivilege)
    else:
        user_privilege_db = db.query(models.UserPrivilege).filter(
            models.UserPrivilege.user_role.any(id=user_db.user_role_id)
        )
    return user_privilege_db.all()
