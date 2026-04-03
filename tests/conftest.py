"""Shared pytest fixtures."""
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.auth_service import AuthService


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def auth_headers(client):
    """Return Authorization headers for the admin user."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "secret"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
