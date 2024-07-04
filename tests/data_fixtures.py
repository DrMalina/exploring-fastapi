import datetime
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


@pytest.fixture(name="raw_todos")
def fx_raw_todos() -> Sequence[Mapping[str, Any]]:
    """Unstructured todos representation."""
    return [
        {
            "id": 1,
            "name": "Clean kitchen",
            "description": "The kitchen needs cleaning, "
            "especially the sink and the fridge.",
            "is_completed": False,
            "is_deleted": False,
            "created_at": datetime.datetime(2024, 7, 3, 12, 0),  # noqa:  DTZ001
            "updated_at": None,
            "todo_category_id": 2,
        },
        {
            "id": 2,
            "name": "Take out trash",
            "description": "Trash can is full.",
            "is_completed": True,
            "is_deleted": False,
            "created_at": datetime.datetime(2024, 7, 3, 13, 0),  # noqa:  DTZ001
            "updated_at": None,
            "todo_category_id": 2,
        },
        {
            "id": 3,
            "name": "Finish Roadmap for Q4",
            "description": "We need to have a general outlines "
            "before the all-hands meeting.",
            "is_completed": False,
            "is_deleted": False,
            "created_at": datetime.datetime(2024, 7, 3, 14, 0),  # noqa:  DTZ001
            "updated_at": None,
            "todo_category_id": 2,
        },
        {
            "id": 4,
            "name": "Review PDP summary",
            "description": "Clarify PDP goals with PM.",
            "is_completed": True,
            "is_deleted": False,
            "created_at": datetime.datetime(2024, 7, 3, 15, 0),  # noqa:  DTZ001
            "updated_at": None,
            "todo_category_id": 2,
        },
    ]
