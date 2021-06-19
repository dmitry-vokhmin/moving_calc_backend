from typing import Optional
from pydantic import BaseModel, validator


class InventoryBase(BaseModel):
    name: str
    height: Optional[float]
    width: Optional[float]
    length: Optional[float]
    inventory_category_id: Optional[int]
    dimension: Optional[float]

    class Config:
        orm_mode = True

    @validator("name")
    def empty_str(cls, v):
        if v == "":
            raise ValueError("Empty string")
        return v


class InventoryCreate(InventoryBase):
    image: Optional[str]


class InventoryGet(InventoryBase):
    id: int
    company_id: Optional[int]
    image: Optional[str]

    @validator('image', always=True)
    def urljoin(cls, image) -> str:
        return f"http://127.0.0.1:8080/{image}"
