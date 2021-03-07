from pydantic import BaseModel, validator


class TruckBase(BaseModel):
    name: str
    truck_type_id: int

    class Config:
        orm_mode = True

    @validator("name")
    def empty_str(cls, v):
        if v == "":
            raise ValueError("Empty string")
        return v


class TruckCreate(TruckBase):
    pass


class TruckGet(TruckBase):
    id: int
