from fastapi import HTTPException
from starlette import status


class TodoCategoryExistsException(HTTPException):
    def __init__(self, name: str) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"TodoCategory with a name '{name}' already exists.",
        )
