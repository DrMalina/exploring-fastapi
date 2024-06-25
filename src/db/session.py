import contextlib
from typing import Any, AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.config import settings
from src.db.exceptions import DbSessionManagerNotInitializedError


class DatabaseSessionManager:
    def __init__(self, host: str, **engine_kwargs: Any) -> None:
        if engine_kwargs is None:
            engine_kwargs = {}
        self._engine: AsyncEngine | None = create_async_engine(host, **engine_kwargs)
        self._sessionmaker: async_sessionmaker[AsyncSession] | None = (
            async_sessionmaker(autocommit=False, bind=self._engine))

    async def close(self) -> None:
        if self._engine is None:
            raise DbSessionManagerNotInitializedError
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise DbSessionManagerNotInitializedError

        async with self._engine.begin() as connection:
            try:
                yield connection
            except DbSessionManagerNotInitializedError:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise DbSessionManagerNotInitializedError

        session = self._sessionmaker()
        try:
            yield session
        except DbSessionManagerNotInitializedError:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(str(settings.DATABASE_ASYNC_URL),
                                        pool_size=settings.DATABASE_POOL_SIZE,
                                        pool_recycle=settings.DATABASE_POOL_TTL,
                                        pool_pre_ping=settings.DATABASE_POOL_PRE_PING)


async def get_db_session() -> AsyncIterator[AsyncSession]:
    async with sessionmanager.session() as session:
        yield session
