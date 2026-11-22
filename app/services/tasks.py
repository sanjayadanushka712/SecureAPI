from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Task
from app.schemas.tasks import TaskCreate


def create_task(db: Session, task_data: TaskCreate):
    new_task = Task(**task_data.model_dump())

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


def get_all_tasks(db: Session):
    statement = select(Task)
    result = db.execute(statement)

    return result.scalars().all()


def get_task_by_id(db: Session, task_id: int):
    return db.get(Task, task_id)


def complete_task(db: Session, task_id: int):
    task = get_task_by_id(db, task_id)

    if task is None:
        return None

    task.completed = True
    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def update_task(db: Session, task_id: int, task_data: TaskCreate):
    task = get_task_by_id(db, task_id)

    if task is None:
        return None

    for field, value in task_data.model_dump().items():
        setattr(task, field, value)

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def delete_task(db: Session, task_id: int):
    task = get_task_by_id(db, task_id)

    if task is None:
        return False

    db.delete(task)
    db.commit()

    return True
