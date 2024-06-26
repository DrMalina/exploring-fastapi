from pydantic import BaseModel, Field


class TodoCategoryCreate(BaseModel):
    name: str = Field(..., max_length=50)


class TodoCategory(BaseModel):
    id: int
    name: str
