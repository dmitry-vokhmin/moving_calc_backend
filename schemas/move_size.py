from pydantic import BaseModel, validator


class MoveSizeBase(BaseModel):
    name: str
    is_extra: bool

    class Config:
        orm_mode = True

    @validator("name")
    def empty_str(cls, v):
        if v == "":
            raise ValueError("Empty string")
        return v


class MoveSizeCreate(MoveSizeBase):
    pass


class MoveSizeGet(MoveSizeBase):
    id: int
