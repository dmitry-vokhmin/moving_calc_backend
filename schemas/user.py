import re
from typing import Optional
from pydantic import BaseModel, EmailStr, SecretStr, validator
from schemas.user_role import UserRoleGet


class UserBase(BaseModel):
    fullname: str
    email: EmailStr
    company_id: Optional[int]
    user_role_id: Optional[int]

    @validator("fullname")
    def empty_str(cls, v):
        if v == "":
            raise ValueError("Empty string")
        return v

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: SecretStr

    @validator("password")
    def valid_password(cls, v):
        password = v.get_secret_value()
        if len(password) < 8:
            raise ValueError("Make sure your password is at least 8 letters")
        if re.search("[a-z]", password) is None:
            raise ValueError("Make sure your password has at least 1 lowercase letter")
        if re.search("[A-Z]", password) is None:
            raise ValueError("Make sure your password has at least 1 capital letter")
        if re.search("[0-9]", password) is None:
            raise ValueError("Make sure your password has at least 1 digit")
        if re.search("\s", password):
            raise ValueError("Make sure your password does not have whitespace characters")
        return v


class UserAuth(BaseModel):
    email: str
    password: SecretStr


class UserUpdate(UserCreate):
    old_password: Optional[SecretStr]
    password: Optional[SecretStr]
    email: Optional[EmailStr]
    id: int


class UserGet(UserBase):
    id: int
    user_role: UserRoleGet
