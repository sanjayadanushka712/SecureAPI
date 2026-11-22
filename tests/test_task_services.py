from app.db.models import Task
from app.schemas.tasks import TaskCreate
from app.services.tasks import create_task, get_task_by_id


def test_create_task(db_session):
    created = create_task(db_session, TaskCreate(title="Learn Python"))

    assert created.id == 1
    assert created.title == "Learn Python"
    assert created.completed is False
    assert db_session.get(Task, 1) is created


def test_get_task_by_id(db_session):
    created = create_task(db_session, TaskCreate(title="Learn Docker"))

    result = get_task_by_id(db_session, created.id)

    assert result == created


def test_get_missing_task(db_session):
    result = get_task_by_id(db_session, 999)

    assert result is None
