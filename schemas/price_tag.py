from pydantic import BaseModel


class PriceTagBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class PriceTagCreate(PriceTagBase):
    pass


class PriceTagGet(PriceTagBase):
    id: int
