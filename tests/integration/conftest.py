from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import settings
from src.db.base import Base
from src.db.session import get_db_session
from src.main import app


@pytest.fixture(scope="module", name="test_client")
async def fx_test_client() -> AsyncIterator[AsyncClient]:
    """Sets up a FastAPI AsyncClient used for testing.

    This is a client without connection to the testing DB.
    Use it for routes' tests that do not use DB session.

    Yields:
        AsyncClient from httpx.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),  # type: ignore
        base_url="http://testserver",
    ) as ac:
        yield ac


SQLALCHEMY_DATABASE_URL = (
    "postgresql+asyncpg://test-app:test-app@localhost:5434/test-app"
)

# we add "poolclass=NullPool", because the same engine must be shared between
# different loop. See more at https://stackoverflow.com/a/75444607
engine = create_async_engine(str(settings.TEST_DATABASE_ASYNC_URL), poolclass=NullPool)

TestingSessionLocal = async_sessionmaker(autocommit=False, bind=engine)


async def _create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def _drop_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(name="test_client_db")
async def fx_test_client_db() -> AsyncIterator[AsyncClient]:
    """Sets up a FastAPI AsyncClient used for testing with
    a testing DB session.

    Yields:
        AsyncClient from httpx.
    """
    # Prepare clean state of the DB for each test
    await _drop_tables()
    await _create_tables()

    # Dependency override
    async def override_get_db() -> AsyncIterator[AsyncSession]:
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db_session] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),  # type: ignore
        base_url="http://testserver",
    ) as ac:
        yield ac


@pytest.fixture(scope="module", name="anyio_backend")
def fx_anyio_backend() -> str:
    """Specify the backend used for testing using anyio plugin.

    See more at:
    https://anyio.readthedocs.io/en/stable/testing.html#specifying-the-backends-to-run-on
    """
    return "asyncio"
