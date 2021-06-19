from typing import Optional
from pydantic import BaseModel


class TruckTypeBase(BaseModel):
    name: str
    dimension: float
    length: Optional[float]
    height: Optional[float]
    width: Optional[float]

    class Config:
        orm_mode = True


class TruckTypeCreate(TruckTypeBase):
    pass


class TruckTypeUpdate(TruckTypeBase):
    id: int


class TruckTypeGet(TruckTypeBase):
    id: int
