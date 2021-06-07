import sqlalchemy as sa
from app.db.session import Base


class Image(Base):
    __tablename__ = "image"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    url = sa.Column(sa.String, nullable=False, index=True)

    def __repr__(self) -> str:
        return f"Image({self.url})"
