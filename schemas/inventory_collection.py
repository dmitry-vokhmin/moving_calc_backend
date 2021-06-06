from typing import Optional
from pydantic import BaseModel
from .move_size import MoveSizeGet


class InventoryCollectionBase(BaseModel):
    move_size_id: int
    company_id: Optional[int]

    class Config:
        orm_mode = True


class InventoryCollectionCreate(InventoryCollectionBase):
    pass


class InventoryCollectionCreatePersonal(InventoryCollectionBase):
    inventory_id: int


class InventoryCollectionGet(InventoryCollectionBase):
    id: int
    move_size: MoveSizeGet
