from pydantic import BaseModel


class StreetBase(BaseModel):
    street_name: str

    class Config:
        orm_mode = True


class StreetCreate(StreetBase):
    pass


class StreetGet(StreetBase):
    id: int
