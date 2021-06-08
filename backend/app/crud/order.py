from os import stat
from app.models.order import OrderItem, OrderState
from typing import List, Optional
from sqlalchemy.orm import Session
from .base import CRUDBase

from app.models import Order
from app.schemas import OrderCreate, OrderUpdate


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    def add_order_items(self, db: Session, db_obj: Order, items: List[OrderItem]) -> Order:
        db_obj.order_items = items
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_queue(self, db: Session) -> List[Order]:
        return db.query(self.model).filter(self.model.state == OrderState.IN_QUEUE).order_by(self.model.updated_at.asc()).all()

    def add_order_item(self, db: Session, db_obj: Order, item: OrderItem):
        db_obj.order_items.append(item)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return item

    def update_state(self, db: Session, db_obj: Order, state: OrderState) -> Order:
        db_obj.state = state
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


order = CRUDOrder(Order)
