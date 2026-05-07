from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_task():
    response = client.post(
        "/tasks/",
        json={
            "title": "Прочитать главу",
            "description": "Прочитать одну главу книги по Python",
            "complexity": "medium",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Прочитать главу"
    assert "category" in data
    assert "estimated_minutes" in data
