from app.models.menu import Item
from app.schemas.item import ItemCreate
from app import crud
from app.tests.utils.utils import random_lower_string
from sqlalchemy.orm.session import Session


def create_random_item(db: Session) -> Item:
    name = random_lower_string()
    desc = random_lower_string()

    return crud.item.create(db, obj_in=ItemCreate(
        name=name,
        description=desc
    ))
