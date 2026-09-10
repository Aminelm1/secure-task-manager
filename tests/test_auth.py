import os

os.environ["TESTING"] = "1"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_tasks_without_token():
    response = client.get("/tasks")

    assert response.status_code in (401, 403)