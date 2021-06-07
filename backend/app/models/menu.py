import sqlalchemy as sa
from sqlalchemy.orm import relationship
from app.db.session import Base

menu_item = sa.Table(
    'menu_item', Base.metadata, sa.Column(
        'item_id',
        sa.Integer,
        sa.ForeignKey('item.id')),
    sa. Column(
        'menu_id',
        sa.Integer,
        sa.ForeignKey('menu.id')))


class Menu(Base):
    __tablename__ = "menu"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String, index=True)
    current = sa.Column(sa.Boolean, index=True)

    created_at = sa.Column(sa.DateTime(timezone=True),
                           server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime(timezone=True),
                           server_default=sa.func.now(), onupdate=sa.func.now())
    items = relationship("Item", secondary=menu_item, back_populates="menus")


class Item(Base):
    __tablename__ = "item"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String, index=True)
    description = sa.Column(sa.String)
    image_id = sa.Column(sa.ForeignKey("image.id"))

    created_at = sa.Column(sa.DateTime(timezone=True),
                           server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime(timezone=True),
                           server_default=sa.func.now(), onupdate=sa.func.now())
    menus = relationship("Menu", secondary=menu_item, back_populates="items")
    image = relationship("Image")
