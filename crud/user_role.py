from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException
from schemas import user_role as user_role_schema
from security.security import get_user, check_privilege


def create(db: Session, user_role: user_role_schema.UserRoleCreate):
    user_role_db = models.UserRole(**user_role.dict())
    db.add(user_role_db)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e.orig))


def read(db: Session, user_role_id: int):
    user_role_db = db.query(models.UserRole).filter_by(id=user_role_id).first()
    return user_role_db


def get_role_privilege(db: Session, user_id: int):
    user_db = get_user(db, user_id)
    return check_user_role_privilege(db, user_db)


def check_user_role_privilege(db: Session, user_db):
    if check_privilege(db, user_db, "user_management"):
        user_role = db.query(models.UserRole).filter_by(id=user_db.user_role_id).first()
        if user_role.child:
            return get_children(user_role.child[0])


def get_children(user_role_child):
    children = []
    if user_role_child.child:
        children.append(user_role_child)
        children.extend(get_children(user_role_child.child[0]))
        return children
    return [user_role_child]
