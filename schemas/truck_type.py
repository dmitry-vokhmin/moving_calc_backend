from pydantic import BaseModel


class TruckTypeBase(BaseModel):
    price: int
    length: float
    height: float
    width: float

    class Config:
        orm_mode = True


class TruckTypeCreate(TruckTypeBase):
    pass


class TruckTypeGet(TruckTypeBase):
    id: int
