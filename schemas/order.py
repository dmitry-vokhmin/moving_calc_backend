import datetime as dt
from pydantic import BaseModel
from .user import UserGet
from .address import AddressGet
from .move_size import MoveSizeGet
from .services import ServicesGet


class OrderBase(BaseModel):
    move_date: dt.date
    hourly_rate: int
    estimated_cost: float
    create_date: dt.datetime
    user: UserGet
    address: AddressGet
    move_size: MoveSizeGet
    service: ServicesGet

    class Config:
        orm_mode = True


class OrderCreate(OrderBase):
    pass


class OrderGet(OrderBase):
    id: int
