from typing import Optional
from pydantic import BaseModel
from .zip_code import ZipCodeGet


class AddressBase(BaseModel):
    street: Optional[str]
    apartment: Optional[str]

    class Config:
        orm_mode = True


class AddressCreate(AddressBase):
    zip_code_id: int


class AddressGet(AddressBase):
    id: int
    zip_code: ZipCodeGet
