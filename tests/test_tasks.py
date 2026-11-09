import pytest
from fastapi.testclient import TestClient

from app.main import app, tasks


@pytest.fixture(autouse=True)
def reset_tasks():
    tasks.clear()
    yield
    tasks.clear()


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

@pytest.mark.parametrize(
    "payload",
    [
        {"title": "ab"},
        {"title": "x" * 101},
        {},
    ],
)
def test_create_task_rejects_invalid_data(client, payload):
    response = client.post("/tasks", json=payload)

    assert response.status_code == 422

def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to SecureAPI"}


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_list_tasks_is_empty_initially(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_create_task(client):
    response = client.post("/tasks", json={"title": "Buy groceries"})

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "Buy groceries",
        "completed": False,
    }
    assert tasks == [{"id": 1, "title": "Buy groceries", "completed": False}]


def test_create_task_with_completed_true(client):
    response = client.post(
        "/tasks", json={"title": "Write tests", "completed": True}
    )

    assert response.status_code == 201
    assert response.json()["completed"] is True


def test_create_task_rejects_short_title(client):
    response = client.post("/tasks", json={"title": "ab"})

    assert response.status_code == 422


def test_create_task_rejects_long_title(client):
    response = client.post("/tasks", json={"title": "x" * 101})

    assert response.status_code == 422


def test_create_task_rejects_missing_title(client):
    response = client.post("/tasks", json={})

    assert response.status_code == 422


def test_create_task_ids_increment(client):
    first = client.post("/tasks", json={"title": "First task"})
    second = client.post("/tasks", json={"title": "Second task"})

    assert first.json()["id"] == 1
    assert second.json()["id"] == 2


def test_get_task(client):
    created = client.post("/tasks", json={"title": "Read a book"}).json()

    response = client.get(f"/tasks/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_get_task_not_found(client):
    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task with ID 999 not found"}


def test_complete_task(client):
    created = client.post("/tasks", json={"title": "Go for a run"}).json()

    response = client.patch(f"/tasks/{created['id']}/complete")

    assert response.status_code == 200
    assert response.json() == {**created, "completed": True}


def test_complete_task_not_found(client):
    response = client.patch("/tasks/999/complete")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task with ID 999 not found"}


def test_update_task(client):
    created = client.post("/tasks", json={"title": "Old title"}).json()

    response = client.put(
        f"/tasks/{created['id']}",
        json={"title": "New title", "completed": True},
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": created["id"],
        "title": "New title",
        "completed": True,
    }


def test_update_task_not_found(client):
    response = client.put("/tasks/999", json={"title": "New title"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Task with ID 999 not found"}


def test_delete_task(client):
    created = client.post("/tasks", json={"title": "Delete me"}).json()

    response = client.delete(f"/tasks/{created['id']}")

    assert response.status_code == 204
    assert response.content == b""
    assert client.get(f"/tasks/{created['id']}").status_code == 404


def test_delete_task_not_found(client):
    response = client.delete("/tasks/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task with ID 999 not found"}


def test_task_lifecycle(client):
    created = client.post("/tasks", json={"title": "Lifecycle task"}).json()
    task_id = created["id"]

    assert client.get("/tasks").json() == [created]
    assert client.patch(f"/tasks/{task_id}/complete").json()["completed"] is True
    assert client.put(
        f"/tasks/{task_id}", json={"title": "Updated"}
    ).json()["title"] == "Updated"
    assert client.delete(f"/tasks/{task_id}").status_code == 204
    assert client.get("/tasks").json() == []
