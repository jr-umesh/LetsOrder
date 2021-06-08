from enum import Enum
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from app.db.session import Base


class OrderState(str, Enum):
    IN_QUEUE = "in_queue"
    COMPLETE = "complete"
    CANCELED = "canceled"


class Order(Base):
    __tablename__ = "order"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    customer_id = sa.Column(sa.ForeignKey("user.id"))
    # maybe we can created new table for table
    table_id = sa.Column(sa.Integer, nullable=False)
    state = sa.Column(sa.String, nullable=False, index=True,
                      default=OrderState.IN_QUEUE)

    created_at = sa.Column(sa.DateTime(timezone=True),
                           server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime(timezone=True),
                           server_default=sa.func.now(), onupdate=sa.func.now())
    order_items = relationship("OrderItem", back_populates="order")

    def __repr__(self) -> str:
        return f"Order(customer_id:{self.customer_id}, state:{self.state})"


class OrderItem(Base):
    __tablename__ = "order_item"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    item_id = sa.Column(sa.ForeignKey("item.id"), nullable=False)
    order_id = sa.Column(sa.ForeignKey("order.id"), nullable=False)
    quantity = sa.Column(sa.Integer, nullable=False, default=1)

    order = relationship("Order", back_populates="order_items")
    item = relationship("Item")

    def __repr__(self) -> str:
        return f"OrderItem(order_id:{self.order_id}, item_id:{self.item_id})"
