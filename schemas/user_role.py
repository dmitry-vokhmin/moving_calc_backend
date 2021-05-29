from typing import Union
from pydantic import BaseModel, validator


class UserRoleBase(BaseModel):
    role: str
    parent_id: Union[int, None]

    @validator("role")
    def empty_str(cls, v):
        if v == "":
            raise ValueError("Empty string")
        return v

    class Config:
        orm_mode = True


class UserRoleCreate(UserRoleBase):
    pass


class UserRoleGet(UserRoleBase):
    id: int
