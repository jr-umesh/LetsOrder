from typing import Optional
from pydantic import BaseModel
from pydantic.networks import EmailStr

from app.models.user import UserRole


class UserBase(BaseModel):
    email: Optional[EmailStr]
    full_name: Optional[str]


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    password: Optional[str]


class UserInDB(UserBase):
    id: Optional[int]

    class Config:
        orm_mode = True
