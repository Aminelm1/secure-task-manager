import os

os.environ["TESTING"] = "1"

from fastapi.testclient import TestClient

from app.main import app
from app.auth import get_current_user
from app.main import get_db



client = TestClient(app)


def fake_user():
    return {
        "preferred_username": "testuser",
        "realm_access": {
            "roles": ["user"]
        }
    }


def fake_admin():
    return {
        "preferred_username": "adminuser",
        "realm_access": {
            "roles": ["user", "admin"]
        }
    }


def test_user_cannot_access_admin():
    app.dependency_overrides[get_current_user] = fake_user

    response = client.get("/admin")

    assert response.status_code == 403

    app.dependency_overrides.clear()


def test_admin_can_access_admin():
    app.dependency_overrides[get_current_user] = fake_admin

    response = client.get("/admin")

    assert response.status_code == 200

    app.dependency_overrides.clear()

class FakeQuery:
  def all(self):
        return []


class FakeDB:
    def query(self, model):
        return FakeQuery()


def fake_db():
    yield FakeDB()


def test_user_can_access_tasks():
    app.dependency_overrides[get_current_user] = fake_user
    app.dependency_overrides[get_db] = fake_db

    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []

    app.dependency_overrides.clear()