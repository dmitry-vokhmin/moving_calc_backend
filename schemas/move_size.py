from pydantic import BaseModel


class MoveSizeBase(BaseModel):
    name: str

    class Config:
        orm_mode = True

class MoveSizeCreate(MoveSizeBase):
    pass


class MoveSizeGet(MoveSizeBase):
    id: int
