from pydantic import BaseModel
from .user import UserGet


class OrderBase(BaseModel):
    user: UserGet

    class Config:
        orm_mode = True


class OrderCreate(OrderBase):
    pass


class OrderGet(OrderBase):
    id: int
