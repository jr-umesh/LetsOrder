from datetime import datetime
from app.models.order import OrderState
from typing import Optional
from pydantic import BaseModel


class OrderItemBase(BaseModel):
    item_id: Optional[int]
    order_id: Optional[int]
    quantity: Optional[int]


class OrderItemCreate(OrderItemBase):
    item_id: int
    order_id: int


class OrderItemUpdate(OrderItemBase):
    pass


class OrderItemInDB(OrderItemBase):
    id: Optional[int]

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    state: Optional[OrderState]
    table_id: Optional[int]
    customer_id: Optional[int]


class OrderCreate(OrderBase):
    table_id: int
    customer_id: int


class OrderUpdate(OrderBase):
    pass


class OrderInDB(OrderBase):
    id: Optional[int]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class OrderItemRequest(BaseModel):
    item_id: int
    quantity: Optional[int] = 1
