from pydantic import BaseModel


class MoverAmountBase(BaseModel):
    amount: int

    class Config:
        orm_mode = True


class MoverAmountCreate(MoverAmountBase):
    pass


class MoverAmountGet(MoverAmountBase):
    id: int
