from starlette import status

from src.exceptions import CustomHTTPException


class TodoCategoryExistsException(CustomHTTPException):
    def __init__(self, name: str) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            msg=f"TodoCategory with a name '{name}' already exists.",
        )
