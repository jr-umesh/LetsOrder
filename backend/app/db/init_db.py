from app.api.v1.user.user_roles import UserRole
from app.db.session import Base, SessionLocal
from app.db.session import engine

from app import crud, schemas
from app.core.config import settings
from . import base


def init_db() -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        fm = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
        if not fm:
            crud.user.create(db, obj_in=schemas.UserCreate(
                email=settings.FIRST_SUPERUSER_EMAIL,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                role=UserRole.MANAGER
            ))
