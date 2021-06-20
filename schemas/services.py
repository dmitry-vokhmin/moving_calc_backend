from pydantic import BaseModel, validator


class ServicesBase(BaseModel):
    name: str

    class Config:
        orm_mode = True

    @validator("name")
    def empty_str(cls, name):
        if name == "":
            raise ValueError("Empty string")
        return name


class ServicesCreate(ServicesBase):
    pass


class ServicesGet(ServicesBase):
    id: int
