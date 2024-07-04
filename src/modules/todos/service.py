from collections.abc import Sequence

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import CouldNotReturnCreatedDBRecordError
from src.modules.todos.models import Todo
from src.modules.todos.schemas import TodoCreate


class TodoService:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def create(self, todo: TodoCreate) -> Todo:
        result = await self.db_session.scalar(
            insert(Todo).values(**todo.model_dump()).returning(Todo)
        )
        await self.db_session.commit()
        await self.db_session.refresh(result)

        if not result:
            raise CouldNotReturnCreatedDBRecordError(str(Todo.name))

        return result

    async def get_all(self) -> Sequence[Todo]:
        results = await self.db_session.scalars(select(Todo))
        return results.all()
