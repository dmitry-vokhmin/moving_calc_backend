from pydantic import BaseModel


class InventoryCollectionBase(BaseModel):
    move_size_id: int

    class Config:
        orm_mode = True


class InventoryCollectionCreate(InventoryCollectionBase):
    pass


class InventoryCollectionGet(InventoryCollectionBase):
    id: int

