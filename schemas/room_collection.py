from pydantic import BaseModel, validator


class RoomCollectionsBase(BaseModel):
    name: str

    class Config:
        orm_mode = True

    @validator("name")
    def empty_str(cls, v):
        if v == "":
            raise ValueError("Empty string")
        return v


class RoomCollectionsCreate(RoomCollectionsBase):
    pass


class RoomCollectionsGet(RoomCollectionsBase):
    id: int
    preset: bool
