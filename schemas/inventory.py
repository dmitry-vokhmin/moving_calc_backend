from pydantic import BaseModel


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


class InventoryCreate(InventoryBase):
    pass


class InventoryGet(InventoryBase):
    id: int
