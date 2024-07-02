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
