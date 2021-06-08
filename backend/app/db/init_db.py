from app.db.session import Base, SessionLocal
from app.db.session import engine

from app import crud, schemas, models
from app.core.config import settings
from . import base


def init_db() -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:

        # setup default image that all user get initially
        # this requires that we store an image in the folder according to
        default_pic = crud.image.get_by_url(db, url=settings.DEFAULT_IMG_URL)
        if not default_pic:
            crud.image.create(db, obj_in=schemas.ImageCreate(
                url=settings.DEFAULT_IMG_URL,
            ))

        # create the first manager
        fm = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
        if not fm:
            su = crud.user.create(db, obj_in=schemas.UserCreate(
                email=settings.FIRST_SUPERUSER_EMAIL,
                full_name="superuser",
                password=settings.FIRST_SUPERUSER_PASSWORD,
            ))
            crud.user.set_role(db, db_obj=su, role=models.UserRole.MANAGER)
