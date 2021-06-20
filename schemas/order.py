import datetime as dt
from typing import List
from pydantic import BaseModel
from .user_client import UserGet
from .address import AddressGet
from .floor_collection import FloorCollectionGet
from .services import ServicesGet


class OrderBase(BaseModel):
    move_date: dt.date
    hourly_rate: int
    estimated_cost: str
    estimated_hours: str
    travel_time: int
    crew_size: int
    truck_size: int

    class Config:
        orm_mode = True


class OrderCreate(OrderBase):
    user_id: int
    address_from_id: int
    address_to_id: int
    floor_collection_from_id: int
    floor_collection_to_id: int
    move_size_id_list: List[int]
    service_id: int


class OrderGet(OrderBase):
    id: int
    user: UserGet
    address_from: AddressGet
    address_to: AddressGet
    floor_collection_from: FloorCollectionGet
    floor_collection_to: FloorCollectionGet
    service: ServicesGet
