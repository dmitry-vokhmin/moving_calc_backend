from datetime import date
from typing import Optional
from pydantic import BaseModel
from .price_tag import PriceTagGet


class CalendarBase(BaseModel):
    start_date: date
    end_date: date

    class Config:
        orm_mode = True


class CalendarCreate(CalendarBase):
    price_tag_id: int


class CalendarGet(CalendarBase):
    id: int
    price_tag: PriceTagGet


class CalendarUpdate(CalendarBase):
    price_tag_id: Optional[date]
