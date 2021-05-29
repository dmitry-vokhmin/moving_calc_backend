from pydantic import BaseModel, validator


class CompanyBase(BaseModel):
    name: str

    class Config:
        orm_mode = True

    @validator("name")
    def empty_str(cls, v):
        if v == "":
            raise ValueError("Empty string")
        return v


class CompanyCreate(CompanyBase):
    pass


class CompanyGet(CompanyBase):
    id: int
