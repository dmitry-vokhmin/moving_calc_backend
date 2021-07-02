from pydantic import BaseModel, validator


class RoomBase(BaseModel):
    name: str

    class Config:
        orm_mode = True

    @validator("name")
    def empty_str(cls, name):
        if name == "":
            raise ValueError("Empty string")
        return name


class RoomCreate(RoomBase):
    pass


class RoomCategoryCreate(BaseModel):
    room_id: int
    category_id: int


class RoomGet(RoomBase):
    id: int
