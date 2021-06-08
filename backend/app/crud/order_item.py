from typing import Optional
from sqlalchemy.orm import Session
from .base import CRUDBase

from app.models import OrderItem
from app.schemas import OrderItemCreate, OrderItemUpdate


class CRUDOrderItem(CRUDBase[OrderItem, OrderItemCreate, OrderItemUpdate]):
    def get_by_url(self, db: Session, url: str) -> Optional[OrderItem]:
        return db.query(self.model).filter(self.model.url == url).first()


order_item = CRUDOrderItem(OrderItem)
