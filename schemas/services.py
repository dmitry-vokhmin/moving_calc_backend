from pydantic import BaseModel, validator


class ServicesBase(BaseModel):
    name: str

    class Config:
        orm_mode = True

    @validator("name")
    def empty_str(cls, v):
        if v == "":
            raise ValueError("Empty string")
        return v


class ServicesCreate(ServicesBase):
    pass


class ServicesGet(ServicesBase):
    id: int
