from pydantic import BaseModel
from .price_tag_name import PriceTagNameGet


class PriceTagBase(BaseModel):
    price: int

    class Config:
        orm_mode = True


class PriceTagCreate(PriceTagBase):
    price_tag_name_id: int


class PriceTagGet(PriceTagBase):
    id: int
    user_id: int
    price_tag_name: PriceTagNameGet
