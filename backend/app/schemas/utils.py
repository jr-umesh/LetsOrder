from typing import Optional
from pydantic import BaseModel


class ImageBase(BaseModel):
    url: Optional[str]


class ImageCreate(ImageBase):
    url: str


class ImageUpdate(ImageBase):
    pass


class ImageInDB(ImageBase):
    id: Optional[int]

    class Config:
        orm_mode = True
