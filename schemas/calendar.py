from pydantic import BaseModel
from datetime import date


class CalendarBase(BaseModel):
    start_date: date
    end_date: date

    class Config:
        orm_mode = True


class CalendarCreate(CalendarBase):
    pass


class CalendarGet(CalendarBase):
    id: int
    price_tag_id: int
