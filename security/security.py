import datetime as dt
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from data_base.database import get_db
from data_base.models import User


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "adsfagjhakjdbagcvuiowqiuDFJKJHDASOKJHADFIJEWNVKLAKJLWEFAJP"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authorization")


def get_secret_hash(plain_password):
    return password_context.hash(plain_password)


def verify_secret(plain_password, hash_password):
    return password_context.verify(plain_password, hash_password)


def create_access_token(user, expires_delta=dt.timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)):
    expire = dt.datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "id": user.id}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter_by(id=user_id).first()
    return user
