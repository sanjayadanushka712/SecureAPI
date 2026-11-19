from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(
        min_length=3,
        max_length=100,
        examples=["Buy groceries"],
    )
    completed: bool = False


class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool
