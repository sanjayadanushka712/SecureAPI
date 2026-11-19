from fastapi import APIRouter, HTTPException, status
from app.schemas.tasks import TaskCreate, TaskResponse
from app.services.tasks import (
    create_task,
    get_all_tasks,
    get_task_by_id,
    complete_task,
    update_task,
    delete_task,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])

tasks = []


@router.get("/", response_model=list[TaskResponse])
def get_tasks():
    return get_all_tasks(tasks)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    task = get_task_by_id(tasks, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )

    return task


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task_route(task_data: TaskCreate):
    return create_task(tasks, task_data)


@router.patch("/{task_id}/complete", response_model=TaskResponse)
def complete_task_route(task_id: int):
    task = complete_task(tasks, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )

    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task_route(task_id: int, task_data: TaskCreate):
    task = update_task(tasks, task_id, task_data)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_route(task_id: int):
    deleted = delete_task(tasks, task_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
