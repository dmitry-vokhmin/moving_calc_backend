from pydantic import BaseModel


class InventoryCollectionBase(BaseModel):
    preset: bool

    class Config:
        orm_mode = True


class InventoryCollectionCreate(InventoryCollectionBase):
    pass


class InventoryCollectionGet(InventoryCollectionBase):
    id: int

