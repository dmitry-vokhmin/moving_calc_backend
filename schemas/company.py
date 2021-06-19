from pydantic import BaseModel, validator
from schemas.address import AddressGet


class CompanyBase(BaseModel):
    name: str

    class Config:
        orm_mode = True

    @validator("name")
    def empty_str(cls, name):
        if name == "":
            raise ValueError("Empty string")
        return name


class CompanyCreate(CompanyBase):
    street: str
    apartment: str
    zip_code: str
    city: str
    state: str


class CompanyGet(CompanyBase):
    id: int
    address: AddressGet
