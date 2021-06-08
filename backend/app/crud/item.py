from app.models.image import Image
from typing import Optional
from sqlalchemy.orm import Session
from .base import CRUDBase

from app.models import Item
from app.schemas import ItemCreate, ItemUpdate


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    def get_menu(self, db: Session):
        return db.query(self.model).filter(self.model.in_menu).all()

    def remove_from_menu(self, db: Session, db_obj: Item):
        db_obj.in_menu = False
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def change_image(self, db: Session, db_obj: Item, image: Image):
        db_obj.image = image
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)


item = CRUDItem(Item)
