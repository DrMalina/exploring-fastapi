from starlette import status

from src.exceptions import CustomHTTPErrorDetail, CustomHTTPException


class TodoCategoryNotFound(CustomHTTPException):
    def __init__(self, todo_category_id: int, loc: tuple[int | str, ...]) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_details=[
                CustomHTTPErrorDetail(
                    msg="The TodoCategory does not exist.",
                    loc=loc,
                    type="not_found",
                    input=todo_category_id,
                )
            ],
        )


class TodoCategoryAlreadyExists(CustomHTTPException):
    def __init__(self, todo_category_name: str, loc: tuple[int | str, ...]) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            error_details=[
                CustomHTTPErrorDetail(
                    msg="A TodoCategory with that name already exists.",
                    loc=loc,
                    type="exists",
                    input=todo_category_name,
                )
            ],
        )
