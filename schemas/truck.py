from pydantic import BaseModel


class TruckBase(BaseModel):
    name: str

    class Config:
        orm_mode = True

class TruckCreate(TruckBase):
    pass


class TruckGet(TruckBase):
    id: int
    truck_type_id: int
