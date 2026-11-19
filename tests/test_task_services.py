import pytest

from app.schemas.tasks import TaskCreate
from app.services.tasks import create_task, get_task_by_id


@pytest.fixture
def task_list():
    return []


def test_create_task(task_list):
    task_data = TaskCreate(title="Learn Python")

    result = create_task(task_list, task_data)

    assert result == {
        "id": 1,
        "title": "Learn Python",
        "completed": False,
    }

    assert len(task_list) == 1


def test_get_task_by_id(task_list):
    task_data = TaskCreate(title="Learn Docker")
    created = create_task(task_list, task_data)

    result = get_task_by_id(task_list, created["id"])

    assert result == created


def test_get_missing_task(task_list):
    result = get_task_by_id(task_list, 999)

    assert result is None
