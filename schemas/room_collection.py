from pydantic import BaseModel
from schemas.room import RoomGet


class RoomCollectionsBase(BaseModel):
    room_id: int

    class Config:
        orm_mode = True


class RoomCollectionsCreate(RoomCollectionsBase):
    pass


class RoomCollectionsInventoryCreate(BaseModel):
    inventory_name: str
    room_collection_id: int


class RoomCollectionsGet(RoomCollectionsBase):
    id: int
    rooms: RoomGet
