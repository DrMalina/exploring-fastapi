import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.anyio


async def test_create__is_unique__creates_and_returns_record(
    test_client_db: AsyncClient,
) -> None:
    response = await test_client_db.post("/api/todo-categories/", json={"name": "Work"})
    assert response.status_code == 201
    assert response.json() == {"id": 1, "name": "Work"}


async def test_create__already_exists__raises_validation_exception(
    test_client_db: AsyncClient,
) -> None:
    response = await test_client_db.post("/api/todo-categories/", json={"name": "Work"})
    assert response.status_code == 201

    response = await test_client_db.post("/api/todo-categories/", json={"name": "Work"})
    assert response.status_code == 409
    assert response.json() == {
        "detail": [
            {
                "input": "Work",
                "loc": ["body", "name"],
                "msg": "A TodoCategory with that name already exists.",
                "type": "exists",
            }
        ]
    }


async def test_create__too_long_name__raises_validation_exception(
    test_client_db: AsyncClient,
) -> None:
    too_long_name = "W" * 51
    response = await test_client_db.post(
        "/api/todo-categories/", json={"name": too_long_name}
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "ctx": {"max_length": 50},
                "input": "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
                "loc": ["body", "name"],
                "msg": "String should have at most 50 characters",
                "type": "string_too_long",
            }
        ]
    }


async def test_get_all__no_records__returns_empty_list(
    test_client_db: AsyncClient,
) -> None:
    response = await test_client_db.get("/api/todo-categories/")
    assert response.status_code == 200
    assert response.json() == []


async def test_get_all__existing_records__returns_list_of_categories(
    test_client_db: AsyncClient,
) -> None:
    work_category_response = await test_client_db.post(
        "/api/todo-categories/", json={"name": "Work"}
    )
    assert work_category_response.status_code == 201
    home_category_response = await test_client_db.post(
        "/api/todo-categories/", json={"name": "Home"}
    )
    assert home_category_response.status_code == 201

    response = await test_client_db.get("/api/todo-categories/")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Work"}, {"id": 2, "name": "Home"}]


async def test_get__does_not_exist__returns_404(
    test_client_db: AsyncClient,
) -> None:
    non_existing_id = 99
    response = await test_client_db.get(f"/api/todo-categories/{non_existing_id}")
    assert response.status_code == 404
    assert response.json() == {
        "detail": [
            {
                "input": non_existing_id,
                "loc": ["path", "id"],
                "msg": "The TodoCategory does not exist.",
                "type": "not_found",
            }
        ]
    }


async def test_get__exists__returns_record(
    test_client_db: AsyncClient,
) -> None:
    response = await test_client_db.post("/api/todo-categories/", json={"name": "Work"})
    assert response.status_code == 201

    response = await test_client_db.get("/api/todo-categories/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Work"}
