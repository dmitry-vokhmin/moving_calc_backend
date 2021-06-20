from pydantic import BaseModel, validator


class ZipCodeBase(BaseModel):
    zip_code: str
    city: str
    state: str

    class Config:
        orm_mode = True

    @validator("zip_code", "city", "state")
    def empty_str(cls, value):
        if value == "":
            raise ValueError("Empty string")
        return value


class ZipCodeCreate(ZipCodeBase):
    pass


class ZipCodeGet(ZipCodeBase):
    id: int
