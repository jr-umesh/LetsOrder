import sqlalchemy as sa
from app.db.session import Base


class User(Base):
    __tablename__ = "user"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    email = sa.Column(sa.String, index=True, nullable=False, unique=True)
    full_name = sa.Column(sa.String)
    password = sa.Column(sa.String, nullable=False)

    def __repr__(self) -> str:
        return f"User({self.role}, {self.email})"
