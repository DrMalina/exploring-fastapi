from collections.abc import Mapping, Sequence
from typing import Any

import pytest
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.todo_categories.models import TodoCategory as TodoCategoryModel

pytestmark = pytest.mark.anyio


@pytest.fixture(name="_seed_db")
async def _fx_seed_db(
    session: AsyncSession, raw_todo_categories: Sequence[Mapping[str, Any]]
) -> None:
    await session.execute(insert(TodoCategoryModel), raw_todo_categories)


async def test_create__correct_schema__creates_and_returns_todo_record(
    test_client_db: AsyncClient,
    _seed_db: AsyncSession,
) -> None:
    todo = {
        "name": "Clean kitchen",
        "description": "The kitchen needs cleaning, "
        "especially the sink and the fridge.",
        "is_completed": False,
        "todo_category_id": 1,
    }

    response = await test_client_db.post("/api/todos/", json=todo)
    assert response.status_code == 201
    response_json = response.json()
    assert response_json == {
        "id": 1,
        "name": "Clean kitchen",
        "description": "The kitchen needs cleaning, "
        "especially the sink and the fridge.",
        "is_completed": False,
        "is_deleted": False,
        "created_at": response_json.get("created_at"),
        "updated_at": None,
        "todo_category_id": 1,
        "todo_category": {"id": 1, "name": "Work"},
    }
