from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings


def test_get_image_by_url(db: Session):
    db_obj = crud.image.get_by_url(db, url=settings.DEFAULT_IMG_URL)
    assert db_obj
    assert db_obj.url == settings.DEFAULT_IMG_URL
