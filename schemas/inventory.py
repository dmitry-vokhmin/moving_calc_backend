from typing import Optional, List
from pydantic import BaseModel, validator


class InventoryBase(BaseModel):
    name: str
    height: Optional[float]
    weight: Optional[float]
    width: Optional[float]
    length: Optional[float]
    dimension: float
    unit: Optional[int]

    class Config:
        orm_mode = True

    @validator("name")
    def empty_str(cls, v):
        if v == "":
            raise ValueError("Empty string")
        return v


class InventoryCreate(InventoryBase):
    pass


class InventoryGet(InventoryBase):
    id: int
