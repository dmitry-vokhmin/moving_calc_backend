import random
import string
from sqlalchemy.orm import Session
from data_base import models
from fastapi import HTTPException, status
from schemas import user as user_schema
from security.security import get_secret_hash, verify_secret, get_user
from crud.user_role import get_user_role_children
from utilities.email_template import send_email


def valid_password(user, user_db):
    if user.old_password and user.password:
        if verify_secret(user.old_password.get_secret_value(), user_db.password):
            return True
        else:
            raise HTTPException(status_code=400, detail="Old password does not match")


def allowed_company_and_role(staff_db, user_db, role_children):
    if role_children and \
            user_db.company_id == staff_db.company_id and staff_db.user_role_id in {role.id for role in role_children}:
        return True
    raise HTTPException(status_code=400, detail="Don`t have permissions")


def get_user_and_role_children(db, user_id):
    user_db = get_user(db, user_id)
    role_children = get_user_role_children(db, user_db)
    return user_db, role_children


def one_time_pass(db: Session, email: str, password: str):
    if email and password:
        check_one_time_pass(db, email, password)
    elif email:
        get_one_time_pass(db, email)


def get_one_time_pass(db: Session, email: str):
    user_db = db.query(models.User).filter_by(email=email)
    if user_db.first():
        rand_pass = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=8))
        user_db.update({"one_time_password": get_secret_hash(rand_pass)})
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e.orig))
        send_email(email, rand_pass, user_db.first().fullname)


def check_one_time_pass(db: Session, email,  one_time_pass: str):
    user_db = db.query(models.User).filter_by(email=email)
    user_account = user_db.first()
    if user_account:
        is_pass_valid = verify_secret(one_time_pass, user_account.one_time_password)
        if is_pass_valid:
            return user_db
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect password. Please try again",
        headers={"WWW-Authenticate": "Bearer"})


def reset_password(db: Session, user_data: user_schema.ResetPassword):
    user_db = check_one_time_pass(db, user_data.email, user_data.one_time_password.get_secret_value())
    user_db.update({"password": get_secret_hash(user_data.password.get_secret_value()),
                    "one_time_password": None})
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e.orig))


def add_new_user(db: Session, user: user_schema.UserCreate, user_id: int = None):
    if user_id:
        current_user, role_children = get_user_and_role_children(db, user_id)
        allowed_company_and_role(user, current_user, role_children)
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
    user_db, role_children = get_user_and_role_children(db, user_id)
    staff_db = get_user(db, user.id)
    if (role_children and (user.user_role_id in {role.id for role in role_children}
                           and user_db.company_id == staff_db.company_id)) \
            or (user.id == user_db.id and user.user_role_id == user_db.user_role_id):
        if valid_password(user, user_db):
            user.password = get_secret_hash(user.password.get_secret_value())
        db.query(models.User).filter_by(id=user.id).update({**user.dict(exclude={"old_password", "company_id"},
                                                                        exclude_unset=True)})
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e.orig))
        return db.query(models.User).filter_by(id=user.id).first()
    raise HTTPException(status_code=400, detail="Don`t have permissions")


def read(db: Session, user_id: int):
    user_db = get_user(db, user_id)
    return user_db


def delete(db: Session, user: user_schema.UserGet, user_id: int):
    user_db, role_children = get_user_and_role_children(db, user_id)
    staff_db = get_user(db, user.id)
    allowed_company_and_role(staff_db, user_db, role_children)
    db.query(models.User).filter_by(id=user.id).delete()
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e.orig))


def company_user(db: Session, user_id: int):
    user_db, role_children = get_user_and_role_children(db, user_id)
    if role_children:
        user_db = db.query(models.User).filter_by(company_id=user_db.company_id)
        return user_db.all()
    else:
        raise HTTPException(status_code=400, detail="Not admin of the company")


def read_by_user_email(db: Session, user: user_schema.UserAuth):
    user_db = db.query(models.User).filter_by(email=user.email).first()
    return user_db
