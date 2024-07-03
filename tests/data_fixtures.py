from collections.abc import Mapping, Sequence
from typing import Any

import pytest


@pytest.fixture(name="raw_todo_categories")
def fx_raw_todo_categories() -> Sequence[Mapping[str, Any]]:
    """Unstructured todo-categories representation."""
    return [
        {"id": 1, "name": "Work"},
        {"id": 2, "name": "Home"},
    ]
