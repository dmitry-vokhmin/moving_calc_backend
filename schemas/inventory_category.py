from pydantic import BaseModel, validator


class InventoryCategoryBase(BaseModel):
    name: str

    class Config:
        orm_mode = True

    @validator("name")
    def empty_str(cls, v):
        if v == "":
            raise ValueError("Empty string")
        return v


class InventoryCategoryCreate(InventoryCategoryBase):
    pass


class InventoryCategoryGet(InventoryCategoryBase):
    id: int
