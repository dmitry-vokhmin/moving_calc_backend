from pydantic import BaseModel
from .move_size import MoveSizeGet


class InventoryCollectionBase(BaseModel):
    pass

    class Config:
        orm_mode = True


class InventoryCollectionCreate(InventoryCollectionBase):
    move_size_id: int


class InventoryCollectionGet(InventoryCollectionBase):
    id: int
    move_size: MoveSizeGet
