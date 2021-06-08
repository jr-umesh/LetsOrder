from typing import Optional
from pydantic import BaseModel


class ItemBase(BaseModel):
    name: Optional[str]
    description: Optional[str]
    in_menu: Optional[bool]


class ItemCreate(ItemBase):
    name: str


class ItemUpdate(ItemBase):
    pass


class ItemInDB(ItemBase):
    id: Optional[int]

    class Config:
        orm_mode = True
