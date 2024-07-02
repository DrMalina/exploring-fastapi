from typing import Any, LiteralString

from fastapi import HTTPException
from pydantic import ValidationError
from pydantic_core import InitErrorDetails, PydanticCustomError
from starlette import status


class BaseAppError(Exception):
    pass


class CouldNotReturnCreatedDBRecordError(BaseAppError):
    def __init__(self, record_name: str) -> None:
        super().__init__(
            "Could not return record: " f"'{record_name}' upon writing to the database."
        )


class CustomHTTPException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL_MSG = "Server error"

    def __init__(self, status_code: int | None = None, msg: str | None = None) -> None:
        super().__init__(
            status_code=status_code or self.STATUS_CODE,
            detail=[{"msg": msg or self.DETAIL_MSG}],
        )


class CustomValidationError(BaseAppError):
    def __init__(  # noqa: PLR0913
        self,
        title: str,
        error_type: LiteralString,
        msg: LiteralString,
        loc: tuple[int | str, ...],
        input_value: Any,
    ) -> None:
        raise ValidationError.from_exception_data(
            title=title,
            line_errors=[
                InitErrorDetails(
                    type=PydanticCustomError(
                        error_type,
                        msg,
                    ),
                    loc=loc,
                    input=input_value,
                )
            ],
        )
