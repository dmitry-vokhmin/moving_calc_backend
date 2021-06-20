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
    def check_phone_number(cls, phone_number):
        try:
            parse_number = parse_phone_number(phone_number, "US")
        except NumberParseException as e:
            raise ValueError('Please provide a valid mobile phone number') from e

        if not is_valid_number(parse_number) or number_type(parse_number) not in MOBILE_NUMBER_TYPES:
            raise ValueError('Please provide a valid mobile phone number')

        return format_number(parse_number, PhoneNumberFormat.E164)
        # PhoneNumberFormat.NATIONAL if n.country_code == 1 else PhoneNumberFormat.INTERNATIONAL

    @validator("firstname", "lastname")
    def empty_str(cls, value):
        if value == "":
            raise ValueError("Empty string")
        return value

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    pass


class UserGet(UserBase):
    id: int
