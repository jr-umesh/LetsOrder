import sqlalchemy as sa
from sqlalchemy.orm import relationship
from app.db.session import Base


class Order(Base):
    __tablename__ = "order"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    customer_id = sa.Column(sa.ForeignKey("user.id"))
    state = sa.Column(sa.String, nullable=False, index=True)

    order_items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_item"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    item_id = sa.Column(sa.ForeignKey("item.id"))
    order_id = sa.Column(sa.ForeignKey("order.id"))

    order = relationship("Order", back_populates="order_items")
    item = relationship("Item")
