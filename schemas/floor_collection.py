from pydantic import BaseModel


class FloorCollectionBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class FloorCollectionCreate(FloorCollectionBase):
    pass


class FloorCollectionGet(FloorCollectionBase):
    id: int
