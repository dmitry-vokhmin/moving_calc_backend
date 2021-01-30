from pydantic import BaseModel


class ServicesBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class ServicesCreate(ServicesBase):
    pass


class ServicesGet(ServicesBase):
    id: int
