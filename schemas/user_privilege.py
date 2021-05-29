from pydantic import BaseModel, validator


class UserPrivilegeBase(BaseModel):
    privilege: str

    @validator("privilege")
    def empty_str(cls, v):
        if v == "":
            raise ValueError("Empty string")
        return v

    class Config:
        orm_mode = True


class UserPrivilegeCreate(UserPrivilegeBase):
    pass


class UserPrivilegeGet(UserPrivilegeBase):
    id: int
