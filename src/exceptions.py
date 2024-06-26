from fastapi import HTTPException
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
