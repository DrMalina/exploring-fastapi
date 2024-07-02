from typing import Any, LiteralString

from fastapi import HTTPException
from pydantic import BaseModel, Field, ValidationError
from pydantic_core import InitErrorDetails, PydanticCustomError


class BaseAppError(Exception):
    pass


class CouldNotReturnCreatedDBRecordError(BaseAppError):
    def __init__(self, record_name: str) -> None:
        super().__init__(
            "Could not return record: " f"'{record_name}' upon writing to the database."
        )


class CustomHTTPErrorDetail(BaseModel):
    msg: str
    loc: tuple[int | str, ...]
    error_type: str = Field(..., alias="type")
    input_value: Any | None = Field(None, alias="input")
    ctx: dict | None = None


class CustomHTTPException(HTTPException):
    def __init__(
        self, status_code: int, error_details: list[CustomHTTPErrorDetail]
    ) -> None:
        super().__init__(
            status_code=status_code,
            detail=[
                err_detail.model_dump(exclude_none=True, by_alias=True)
                for err_detail in error_details
            ],
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
