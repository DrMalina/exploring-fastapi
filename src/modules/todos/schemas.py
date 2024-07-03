from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.modules.todo_categories.schemas import TodoCategory


class TodoCreate(BaseModel):
    name: str = Field(..., max_length=50)
    description: str | None = Field(None, max_length=255)
    is_completed: bool = False
    todo_category_id: int


class TodoInDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None
    is_completed: bool = False
    is_deleted: bool = False
    created_at: datetime
    updated_at: datetime | None = None
    todo_category_id: int
    todo_category: TodoCategory


class Todo(TodoInDB): ...
