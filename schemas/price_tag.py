from pydantic import BaseModel, validator


class PriceTagBase(BaseModel):
    name: str
    price: int

    class Config:
        orm_mode = True

    @validator("name")
    def empty_str(cls, v):
        if v == "":
            raise ValueError("Empty string")
        return v


class PriceTagCreate(PriceTagBase):
    pass


class PriceTagGet(PriceTagBase):
    id: int
