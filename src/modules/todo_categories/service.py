from collections.abc import Sequence

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import CouldNotReturnCreatedDBRecordError
from src.modules.todo_categories.models import TodoCategory
from src.modules.todo_categories.schemas import TodoCategoryCreate


class TodoCategoriesService:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def create(self, todo_category: TodoCategoryCreate) -> TodoCategory:
        result = await self.db_session.scalar(
            insert(TodoCategory)
            .values(**todo_category.model_dump())
            .returning(TodoCategory)
        )
        await self.db_session.commit()
        await self.db_session.refresh(result)

        if not result:
            raise CouldNotReturnCreatedDBRecordError(str(TodoCategory.name))
        return result

    async def get_all(self) -> Sequence[TodoCategory]:
        results = await self.db_session.scalars(select(TodoCategory))
        return results.all()

    async def get(self, todo_category_id: int) -> TodoCategory | None:
        stmt = select(TodoCategory).where(TodoCategory.id == todo_category_id)
        return await self.db_session.scalar(stmt)
