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
    image: str


class RoomGet(RoomBase):
    id: int
    image: str

    @validator('image', always=True)
    def urljoin(cls, image) -> str:
        return f"http://127.0.0.1:8080/{image}"
