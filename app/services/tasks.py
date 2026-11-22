from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Task



def create_task(db: Session, task_data):
    new_task = Task(**task_data.model_dump())

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

def get_all_tasks(db: Session):
    statement = select(Task)
    result = db.execute(statement)

    return result.scalars().all()


def get_task_by_id(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task

    return None


def complete_task(tasks, task_id):
    task = get_task_by_id(tasks, task_id)

    if task is None:
        return None

    task["completed"] = True
    return task


def update_task(tasks, task_id, task_data):
    task = get_task_by_id(tasks, task_id)

    if task is None:
        return None

    task.update(task_data.model_dump())
    return task


def delete_task(tasks, task_id):
    task = get_task_by_id(tasks, task_id)

    if task is None:
        return False

    tasks.remove(task)
    return True
