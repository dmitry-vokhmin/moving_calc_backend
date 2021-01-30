from pydantic import BaseModel


class AddressBase(BaseModel):
    house_number: str
    apartment: str

    class Config:
        orm_mode = True


class AddressCreate(AddressBase):
    pass


class AddressGet(AddressBase):
    id: int
    zip_code_id: int
    street_id: int
