from sqlalchemy.orm import Session
from .base import CRUDBase

from app.models import Image
from app.schemas import ImageCreate, ImageUpdate


class CRUDImage(CRUDBase[Image, ImageCreate, ImageUpdate]):
    pass


image = CRUDImage(Image)
