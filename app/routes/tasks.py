from fastapi import APIRouter, HTTPException, status

from app.schemas.tasks import TaskCreate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])

tasks = []


@router.get("/", response_model=list[TaskResponse])
def get_tasks():
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with ID {task_id} not found",
    )


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(task_data: TaskCreate):
    new_id = max((task["id"] for task in tasks), default=0) + 1

    new_task = {
        "id": new_id,
        **task_data.model_dump(),
    }

    tasks.append(new_task)
    return new_task


@router.patch(
    "/{task_id}/complete",
    response_model=TaskResponse,
)
def complete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with ID {task_id} not found",
    )


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskCreate):
    for task in tasks:
        if task["id"] == task_id:
            task.update(task_data.model_dump())
            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with ID {task_id} not found",
    )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with ID {task_id} not found",
    )
