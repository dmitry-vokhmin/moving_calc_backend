from typing import List
from pydantic import BaseModel


class MoverPriceBase(BaseModel):
    price: float
    mover_amount_id: int
    price_tag_id: int

    class Config:
        orm_mode = True


class MoverPriceCreate(MoverPriceBase):
    pass


class MoverPriceUpdate(BaseModel):
    __root__: List[MoverPriceCreate]


class MoverPriceGet(MoverPriceBase):
    id: int
