from typing import Optional
from sqlalchemy.orm import Session
from .base import CRUDBase

from app.models import Image
from app.schemas import ImageCreate, ImageUpdate


class CRUDImage(CRUDBase[Image, ImageCreate, ImageUpdate]):
    def get_by_url(self, db: Session, url: str) -> Optional[Image]:
        return db.query(self.model).filter(self.model.url == url).first()


image = CRUDImage(Image)
