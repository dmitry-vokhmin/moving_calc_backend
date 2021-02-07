from pydantic import BaseModel


class InventoryBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class InventoryCreate(InventoryBase):
    height: float
    weight: float
    width: float
    deep: float
    dimension: float
    unit: int


class InventoryGet(InventoryBase):
    id: int
