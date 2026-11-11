from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="SecureAPI",
    description="A secure backend API platform",
    version="1.0.0",
)


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, examples=["Buy groceries"])
    completed: bool = False


class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool


# Seeded with a single sample task for testing
tasks = []


@app.get("/")
def root():
    return {"message": "Welcome to SecureAPI"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with ID {task_id} not found",
    )


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate):
    new_id = max((task["id"] for task in tasks), default=0) + 1
    new_task = {"id": new_id, **task_data.model_dump()}
    tasks.append(new_task)
    return new_task


@app.patch(
    "/tasks/{task_id}/complete",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
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


@app.put(
    "/tasks/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK
)
def update_task(task_id: int, task_data: TaskCreate):
    for task in tasks:
        if task["id"] == task_id:
            task.update(task_data.model_dump())
            return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with ID {task_id} not found",
    )


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with ID {task_id} not found",
    )
