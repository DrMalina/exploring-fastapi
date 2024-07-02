from pydantic import BaseModel, ConfigDict, Field


class TodoCategoryCreate(BaseModel):
    name: str = Field(..., max_length=50)


class TodoCategoryInDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class TodoCategory(TodoCategoryInDB): ...
