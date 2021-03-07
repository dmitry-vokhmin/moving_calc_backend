from pydantic import BaseModel
from .zip_code import ZipCodeGet
from .street import StreetGet


class AddressBase(BaseModel):
    house_number: str
    apartment: str

    class Config:
        orm_mode = True


class AddressCreate(AddressBase):
    zip_code_id: int
    street: str


class AddressGet(AddressBase):
    id: int
    zip_code: ZipCodeGet
    street: StreetGet
