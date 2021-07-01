from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException, status
from schemas import user_role as user_role_schema
from security.security import get_user, check_privilege


def create(db: Session, user_role: user_role_schema.UserRoleCreate, user_id):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        user_role_db = models.UserRole(**user_role.dict())
        db.add(user_role_db)
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e.orig))
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_role_privilege(db: Session, user_id: int):
    user_db = get_user(db, user_id)
    if user_db.is_staff:
        user_role_db = db.query(models.UserRole).all()
        return user_role_db
    return get_user_role_children(db, user_db)


def get_user_role_children(db: Session, user_db):
    user_role = db.query(models.UserRole).filter_by(id=user_db.user_role_id).first()
    if user_role.child:
        return get_children(user_role.child[0])
    return []


def get_children(user_role_child):
    children = []
    if user_role_child.child:
        children.append(user_role_child)
        children.extend(get_children(user_role_child.child[0]))
        return children
    return [user_role_child]
