from fastapi import FastAPI,HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="SecureAPI",
    description="A secure backend API platform",
    version="1.0.0",
)

class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    completed: bool = False

class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool

tasks = [
    {"id": 1, "title": "Learn FastAPI", "completed": False},
    {"id": 2, "title": "Learn REST APIs", "completed": True},
]

@app.get("/")
def root():
    return {"message": "Welcome to SecureAPI"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/tasks",response_model=list[TaskResponse])
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}",response_model=list[TaskResponse])
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found",
    )

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate):
    new_task = {
        "id": max((task["id"] for task in tasks), default=0) + 1,
        "title": task_data.title,
        "completed": task_data.completed,
    }

    tasks.append(new_task)

    return new_task