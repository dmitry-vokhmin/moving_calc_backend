from pydantic import BaseModel


class MoverPriceBase(BaseModel):
    movers: int
    price: int

    class Config:
        orm_mode = True


class MoverPriceCreate(MoverPriceBase):
    pass


class MoverPriceGet(MoverPriceBase):
    id: int
