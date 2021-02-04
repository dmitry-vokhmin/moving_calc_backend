from pydantic import BaseModel


class ZipCodeBase(BaseModel):
    zip_code: str
    city: str
    state: str

    class Config:
        orm_mode = True


class ZipCodeCreate(ZipCodeBase):
    pass


class ZipCodeGet(ZipCodeBase):
    id: int
