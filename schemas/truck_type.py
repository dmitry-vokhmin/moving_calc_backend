from pydantic import BaseModel


class TruckTypeBase(BaseModel):
    length: float

    class Config:
        orm_mode = True


class TruckTypeCreate(TruckTypeBase):
    price: int
    height: float
    weight: float


class TruckTypeGet(TruckTypeBase):
    id: int
