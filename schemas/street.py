from pydantic import BaseModel, validator


class StreetBase(BaseModel):
    street_name: str

    class Config:
        orm_mode = True

    @validator("street_name")
    def empty_str(cls, v):
        if v == "":
            raise ValueError("Empty string")
        return v


class StreetCreate(StreetBase):
    pass


class StreetGet(StreetBase):
    id: int
