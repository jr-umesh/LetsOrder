
from app.schemas.item import ItemCreate
from app.core.security import verify_password
from app.models.user import UserRole
from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.tests.utils.utils import random_email, random_lower_string


def test_get_menu(
    client: TestClient,
    db: Session
):
    crud.item.create(
        db, obj_in=ItemCreate(
            name=random_lower_string()
        )
    )
    r = client.get(f"{settings.API_PREFIX}/menu")

    assert r.status_code == 200
    menu = r.json()
    assert menu


def test_create_menu_item(
    client: TestClient, superuser_token_headers: Dict[str, str],
    db: Session
):

    name = random_lower_string()
    desc = random_lower_string()
    data = {
        "name": name,
        "description": desc
    }
    r = client.post(f"{settings.API_PREFIX}/menu/",
                    headers=superuser_token_headers, json=data)

    assert r.status_code == 201
    menu_item = r.json()
    assert menu_item
    assert menu_item["name"] == name
    assert menu_item["description"] == desc
    assert menu_item["id"]

    db_obj = crud.item.get(db, menu_item["id"])
    assert db_obj.in_menu


def test_remove_item_from_menu(
    client: TestClient, superuser_token_headers: Dict[str, str],
    db: Session
):
    mi_1 = crud.item.create(
        db, obj_in=ItemCreate(
            name=random_lower_string()
        ))
    r = client.delete(f"{settings.API_PREFIX}/menu/{mi_1.id}",
                      headers=superuser_token_headers)

    assert r.status_code == 200
    menu_item = r.json()
    assert menu_item
    assert menu_item["in_menu"] == False
