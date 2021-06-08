from app.core.security import verify_password
from app.models.user import UserRole
from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.tests.utils.utils import random_email, random_lower_string


def test_register_user(
    client: TestClient, db: Session
):
    email = random_email()
    password = random_lower_string()
    full_name = random_lower_string()
    data = {
        "email": email,
        "password": password,
        "full_name": full_name
    }
    r = client.post(f"{settings.API_PREFIX}/users/register", json=data)
    assert r.status_code == 201
    current_user = r.json()
    assert current_user
    assert current_user["email"] == email
    assert current_user["full_name"] == full_name

    db_obj = crud.user.get_by_email(db, email=email)
    assert db_obj
    assert db_obj.role == UserRole.CUSTOMER
    assert verify_password(password, db_obj.password)


def test_read_user_me(
    client: TestClient, normal_user_token_headers: Dict[str, str]
):
    r = client.get(f"{settings.API_PREFIX}/users/me",
                   headers=normal_user_token_headers)
    assert r.status_code == 200
    current_user = r.json()
    assert current_user
    assert current_user["email"] == settings.TEST_USER_EMAIL


def test_update_user_me(
    client: TestClient, normal_user_token_headers: Dict[str, str]
):

    full_name = random_lower_string()
    data = {
        "full_name": full_name
    }
    r = client.put(f"{settings.API_PREFIX}/users/me",
                   headers=normal_user_token_headers,
                   json=data)
    assert r.status_code == 200
    current_user = r.json()
    assert current_user
    assert current_user["full_name"] == full_name


def test_get_user(
    client: TestClient, normal_user_token_headers: Dict[str, str]
): pass


def test_read_users(
    client: TestClient, normal_user_token_headers: Dict[str, str]
): pass


def test_create_user(
    client: TestClient, normal_user_token_headers: Dict[str, str]
): pass


def test_update_user(
    client: TestClient, normal_user_token_headers: Dict[str, str]
): pass
