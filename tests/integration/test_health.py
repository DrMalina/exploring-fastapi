import pytest
from httpx import AsyncClient


@pytest.mark.anyio()
async def test_health(test_client: AsyncClient) -> None:
    response = await test_client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
