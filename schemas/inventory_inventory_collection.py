from typing import List
from pydantic import BaseModel
from .inventory import InventoryGet


class InventoryInventoryCollectionBase(BaseModel):
    inventory_id: int
    inventory_collection_id: int
    count: int

    class Config:
        orm_mode = True


class InventoryInventoryCollectionCreate(InventoryInventoryCollectionBase):
    pass


class InventoryInventoryCollectionDelete(BaseModel):
    inventory_id: int
    inventory_collection_id: int


class InventoryInventoryCollectionUpdate(BaseModel):
    __root__: List[InventoryInventoryCollectionCreate]


class InventoryInventoryCollectionGet(InventoryInventoryCollectionBase):
    id: int
    inventories: InventoryGet
