from pydantic import BaseModel


class ZipCodeBase(BaseModel):
    city: str
    state: str

    class Config:
        orm_mode = True


class ZipCodeCreate(ZipCodeBase):
    pass


class ZipCodeGet(ZipCodeBase):
    zip_code: int
