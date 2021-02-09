from pydantic import BaseModel


class RoomCollectionsBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class RoomCollectionsCreate(RoomCollectionsBase):
    pass


class RoomCollectionsGet(RoomCollectionsBase):
    id: int
    preset: bool
