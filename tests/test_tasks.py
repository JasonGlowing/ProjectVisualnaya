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


def test_delete_task():
    create_response = client.post(
        "/tasks/",
        json={
            "title": "Удалить задачу",
            "description": "Тестовая задача для удаления",
            "complexity": "low",
        },
    )
    assert create_response.status_code == 200
    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204

    tasks_response = client.get("/tasks/")
    assert tasks_response.status_code == 200
    assert all(task["id"] != task_id for task in tasks_response.json())


def test_delete_missing_task_returns_404():
    response = client.delete("/tasks/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
