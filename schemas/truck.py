from pydantic import BaseModel, validator
from .truck_type import TruckTypeGet


class TruckBase(BaseModel):
    name: str

    class Config:
        orm_mode = True

    @validator("name")
    def empty_str(cls, v):
        if v == "":
            raise ValueError("Empty string")
        return v


class TruckCreate(TruckBase):
    truck_type_id: int


class TruckUpdate(TruckCreate):
    id: int


class TruckGet(TruckBase):
    id: int
    truck_type: TruckTypeGet
    company_id: int
