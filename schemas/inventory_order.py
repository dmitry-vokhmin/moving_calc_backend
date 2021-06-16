from pydantic import BaseModel


class InventoryOrderBase(BaseModel):
    inventory: dict
    order_id: int

    class Config:
        orm_mode = True


class InventoryOrderCreate(InventoryOrderBase):
    pass


class InventoryOrderGet(InventoryOrderBase):
    id: int
