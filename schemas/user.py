from phonenumbers import (
    NumberParseException,
    PhoneNumberFormat,
    PhoneNumberType,
    format_number,
    is_valid_number,
    number_type,
    parse as parse_phone_number,
)
from pydantic import BaseModel, EmailStr, constr, validator

MOBILE_NUMBER_TYPES = PhoneNumberType.MOBILE, PhoneNumberType.FIXED_LINE_OR_MOBILE


class UserBase(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    pass


class UserGet(UserBase):
    id: int
