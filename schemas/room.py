from pydantic import BaseModel, validator
from config import DOMAIN


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
    image: str


class RoomCategoryCreate(BaseModel):
    room_id: int
    category_id: int


class RoomGet(RoomBase):
    id: int
    image: str

    @validator('image', always=True)
    def urljoin(cls, image) -> str:
        return f"{DOMAIN}{image}"
