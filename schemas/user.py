import re
from pydantic import BaseModel, EmailStr, SecretStr, validator


class UserBase(BaseModel):
    username: str
    email: EmailStr

    @validator("username")
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
        if re.search("[@$!#%*?&]", password) is None:
            raise ValueError("At least 1 character from  @$!#%*?&")
        if re.search("\s", password):
            raise ValueError("Make sure your password does not have whitespace characters")
        return v


class UserAuth(BaseModel):
    username: str
    password: SecretStr


class UserGet(UserBase):
    id: int
    is_staff: bool
