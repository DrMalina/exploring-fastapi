from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from typing import Any

import pytest
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.todo_categories.models import TodoCategory as TodoCategoryModel
from src.modules.todos.models import Todo as TodoModel
from src.modules.todos.schemas import TodoCreate

pytestmark = pytest.mark.anyio


@pytest.fixture(name="_seed_todo_categories")
async def _fx_seed_todo_categories(
    session: AsyncSession,
    raw_todo_categories: Sequence[Mapping[str, Any]],
) -> None:
    await session.execute(insert(TodoCategoryModel), raw_todo_categories)


@pytest.fixture(name="_seed_todos")
async def _fx_seed_todos(
    session: AsyncSession,
    raw_todo_categories: Sequence[Mapping[str, Any]],
    raw_todos: Sequence[Mapping[str, Any]],
) -> None:
    # we also need to seed todo-categories due to relationship between those 2
    await session.execute(insert(TodoCategoryModel), raw_todo_categories)
    await session.execute(insert(TodoModel), raw_todos)


@pytest.fixture(name="todo_create")
def fx_todo_create() -> TodoCreate:
    return TodoCreate(
        name="Verify CL from @test",
        description="Review changes in order to close the PBI.",
        is_completed=False,
        todo_category_id=1,
    )


async def test_create__correct_schema__creates_and_returns_todo_record(
    test_client_db: AsyncClient,
    todo_create: TodoCreate,
    _seed_todo_categories: None,
) -> None:
    response = await test_client_db.post("/api/todos/", json=todo_create.model_dump())
    assert response.status_code == 201
    response_json = response.json()
    assert response_json == {
        "id": 1,
        "name": "Verify CL from @test",
        "description": "Review changes in order to close the PBI.",
        "is_completed": False,
        "is_deleted": False,
        "created_at": response_json.get("created_at"),
        "updated_at": None,
        "todo_category_id": 1,
        "todo_category": {"id": 1, "name": "Work"},
    }
    # check if data matches without milliseconds to account
    # for the DB persistence vs test case diff
    now = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S")
    assert now in response_json["created_at"]


async def test_create__not_existing_todo_category__raises_404(
    test_client_db: AsyncClient,
    todo_create: TodoCreate,
) -> None:
    response = await test_client_db.post("/api/todos/", json=todo_create.model_dump())
    assert response.status_code == 404
    assert response.json() == {
        "detail": [
            {
                "msg": "The TodoCategory does not exist.",
                "loc": ["body", "todo_category_id"],
                "type": "not_found",
                "input": 1,
            }
        ]
    }


async def test_get_all__existing_todos__returns_all_todos(
    test_client_db: AsyncClient, _seed_todos: None
) -> None:
    response = await test_client_db.get("/api/todos/")
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json) == 4
    assert response_json[0] == {
        "id": 1,
        "name": "Clean kitchen",
        "description": "The kitchen needs cleaning, "
        "especially the sink and the fridge.",
        "is_completed": False,
        "is_deleted": False,
        "created_at": "2024-07-03T12:00:00",
        "updated_at": None,
        "todo_category_id": 2,
        "todo_category": {"id": 2, "name": "Home"},
    }


async def test_get_all__no_existing_todos__returns_empty_list(
    test_client_db: AsyncClient,
) -> None:
    response = await test_client_db.get("/api/todos/")
    assert response.status_code == 200
    assert response.json() == []
