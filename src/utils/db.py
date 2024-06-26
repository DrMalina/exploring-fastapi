from sqlalchemy.exc import IntegrityError


def is_unique_validation_integrity_error(integrity_err: IntegrityError) -> bool:
    return "UniqueViolationError" in str(integrity_err)
