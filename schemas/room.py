from pydantic import BaseModel, validator


class RoomBase(BaseModel):
    name: str

    class Config:
        orm_mode = True

    @validator("name")
    def empty_str(cls, v):
        if v == "":
            raise ValueError("Empty string")
        return v


class RoomCreate(RoomBase):
    pass


class RoomGet(RoomBase):
    id: int
