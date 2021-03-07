from pydantic import BaseModel, validator


class InventoryBase(BaseModel):
    name: str
    height: float
    weight: float
    width: float
    deep: float
    dimension: float
    unit: int

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
