import sqlalchemy as sa
from sqlalchemy.orm import relationship
from app.db.session import Base


class Item(Base):
    __tablename__ = "item"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String, index=True, nullable=False)
    description = sa.Column(sa.String)
    image_id = sa.Column(sa.ForeignKey("image.id"))
    in_menu = sa.Column(sa.Boolean, default=True)  # if item in menu

    created_at = sa.Column(sa.DateTime(timezone=True),
                           server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime(timezone=True),
                           server_default=sa.func.now(), onupdate=sa.func.now())
    image = relationship("Image")

    def __repr__(self) -> str:
        return f"Item({self.name}, {'in menu' if self.in_menu else 'no in menu'})"
