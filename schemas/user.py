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
    phone_number: constr(max_length=50, strip_whitespace=True)

    @validator('phone_number')
    def check_phone_number(cls, v):
        try:
            n = parse_phone_number(v, "US")
        except NumberParseException as e:
            raise ValueError('Please provide a valid mobile phone number') from e

        if not is_valid_number(n) or number_type(n) not in MOBILE_NUMBER_TYPES:
            raise ValueError('Please provide a valid mobile phone number')

        return format_number(n, PhoneNumberFormat.NATIONAL if n.country_code == 1 else PhoneNumberFormat.INTERNATIONAL)

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    pass


class UserGet(UserBase):
    id: int
