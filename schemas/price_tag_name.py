from pydantic import BaseModel, validator


class PriceTagNameBase(BaseModel):
    name: str

    class Config:
        orm_mode = True

    @validator("name")
    def empty_str(cls, v):
        if v == "":
            raise ValueError("Empty string")
        return v


class PriceTagNameCreate(PriceTagNameBase):
    pass


class PriceTagNameGet(PriceTagNameBase):
    id: int
