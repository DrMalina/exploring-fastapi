from typing import Any

import pytest

from src.modules.todo_categories.schemas import TodoCategory


@pytest.fixture(name="raw_todo_categories")
def fx_raw_todo_categories() -> list[TodoCategory | dict[str, Any]]:
    """Unstructured todo-categories representation."""
    return [
        {"id": 1, "name": "Work"},
        {"id": 2, "name": "Home"},
    ]
