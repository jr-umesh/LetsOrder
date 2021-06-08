from app.schemas.order import OrderCreate, OrderItemCreate
from re import A
from app.models.order import OrderState
from random import randint
from app.schemas.item import ItemCreate
from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.tests.utils.utils import random_lower_string
from app.tests.utils.item import create_random_item


def test_place_an_order(
    client: TestClient, normal_user_token_headers: Dict[str, str],
    db: Session
):

    item1 = create_random_item(db)
    item2 = create_random_item(db)
    table_id = randint(1, 100)

    data = {"items": [
        {
            "item_id": item1.id,
        },
        {
            "item_id": item2.id,
        }
    ],
        "table_id": table_id}

    r = client.post(f"{settings.API_PREFIX}/orders/",
                    headers=normal_user_token_headers,
                    json=data)

    assert r.status_code == 201
    order = r.json()
    assert order["table_id"] == table_id
    assert order["state"] == OrderState.IN_QUEUE


def test_get_order_queue(
    client: TestClient, superuser_token_headers: Dict[str, str],
    db: Session
):
    r = client.get(f"{settings.API_PREFIX}/orders/queue",
                   headers=superuser_token_headers)

    assert r.status_code == 200


def test_add_new_order_item(
    client: TestClient, superuser_token_headers: Dict[str, str],
    db: Session
):
    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
    order = crud.order.create(db, obj_in=OrderCreate(
        table_id=randint(1, 100),
        customer_id=user.id
    ))
    item1 = create_random_item(db)
    data = {
        "item_id": item1.id,
    }
    r = client.post(f"{settings.API_PREFIX}/orders/{order.id}/items",
                    headers=superuser_token_headers, json=data)
    assert r.status_code == 201
    order_item = r.json()
    assert order_item


def test_remove_order_item(
    client: TestClient, superuser_token_headers: Dict[str, str],
    db: Session
):
    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
    order = crud.order.create(db, obj_in=OrderCreate(
        table_id=randint(1, 100),
        customer_id=user.id
    ))
    item1 = create_random_item(db)
    o_item1 = crud.order_item.create(db, obj_in=OrderItemCreate(
        item_id=item1.id,
        order_id=order.id,
    ))
    crud.order.add_order_item(db, db_obj=order, item=o_item1)
    r = client.delete(f"{settings.API_PREFIX}/orders/{order.id}/items/{o_item1.id}",
                      headers=superuser_token_headers)
    assert r.status_code == 200
    order_item = r.json()
    assert order_item
    assert item1 not in order.order_items


def test_order_cancel(
    client: TestClient, superuser_token_headers: Dict[str, str],
    db: Session
):
    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
    order = crud.order.create(db, obj_in=OrderCreate(
        table_id=randint(1, 100),
        customer_id=user.id
    ))
    item1 = create_random_item(db)
    o_item1 = crud.order_item.create(db, obj_in=OrderItemCreate(
        item_id=item1.id,
        order_id=order.id,
    ))
    crud.order.add_order_item(db, db_obj=order, item=o_item1)
    r = client.put(f"{settings.API_PREFIX}/orders/{order.id}/cancel",
                   headers=superuser_token_headers)
    assert r.status_code == 200
    order = r.json()
    assert order
    assert order["state"] == OrderState.CANCELED


def test_order_mark_complete(
    client: TestClient, superuser_token_headers: Dict[str, str],
    db: Session
):
    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
    order = crud.order.create(db, obj_in=OrderCreate(
        table_id=randint(1, 100),
        customer_id=user.id
    ))
    item1 = create_random_item(db)
    o_item1 = crud.order_item.create(db, obj_in=OrderItemCreate(
        item_id=item1.id,
        order_id=order.id,
    ))
    crud.order.add_order_item(db, db_obj=order, item=o_item1)
    r = client.put(f"{settings.API_PREFIX}/orders/{order.id}/complete",
                   headers=superuser_token_headers)
    assert r.status_code == 200
    order = r.json()
    assert order
    assert order["state"] == OrderState.COMPLETE
