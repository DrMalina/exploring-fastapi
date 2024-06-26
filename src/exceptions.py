class BaseAppError(Exception):
    pass


class CouldNotReturnCreatedDBRecordError(BaseAppError):
    def __init__(self, record_name: str) -> None:
        super().__init__(
            "Could not return record: " f"'{record_name}' upon writing to the database."
        )
