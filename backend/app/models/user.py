from enum import Enum
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from app.db.session import Base


class UserRole(str, Enum):
    CUSTOMER = "customer"
    WAITER = "waiter"
    COOK = "cook"
    MANAGER = "manager"


class User(Base):
    __tablename__ = "user"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    email = sa.Column(sa.String, index=True, nullable=False, unique=True)
    full_name = sa.Column(sa.String)
    password = sa.Column(sa.String, nullable=False)
    is_active = sa.Column(sa.Boolean, default=True)
    role = sa.Column(sa.String, default=UserRole.CUSTOMER)
    profile_pic_id = sa.Column(sa.ForeignKey("image.id"))

    profile_pic = relationship("Image")

    def __repr__(self) -> str:
        return f"User({self.full_name}, {self.role})"
