import datetime as dt
from pydantic import BaseModel
from .user import UserGet
from .address import AddressGet
from .floor_collection import FloorCollectionGet
from .services import ServicesGet
from .move_size import MoveSizeGet


class OrderBase(BaseModel):
    move_date: dt.date
    hourly_rate: int
    estimated_cost: str
    estimated_hours: str
    travel_time: int
    movers: int
    truck_type: int


    class Config:
        orm_mode = True


class OrderCreate(OrderBase):
    user_id: int
    address_from_id: int
    address_to_id: int
    floor_collection_from_id: int
    floor_collection_to_id: int
    move_size_id: int
    service_id: int


class OrderGet(OrderBase):
    id: int
    user: UserGet
    address_from: AddressGet
    address_to: AddressGet
    floor_collection_from: FloorCollectionGet
    floor_collection_to: FloorCollectionGet
    move_size: MoveSizeGet
    service: ServicesGet
