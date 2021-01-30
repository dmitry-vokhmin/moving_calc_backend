from pydantic import BaseModel


class InventoryBase(BaseModel):

    name: str
    height: float
    weight: float

    class Config:
        orm_mode = True


class InventoryCreate(InventoryBase):
    width: float
    deep: float
    dimension: float
    unit: int


class InventoryGet(InventoryBase):
    id: int
