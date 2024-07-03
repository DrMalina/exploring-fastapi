from typing import Annotated

from fastapi import Depends

from src.dependencies import DBSessionDep
from src.modules.todo_categories.exceptions import TodoCategoryNotFound
from src.modules.todo_categories.models import TodoCategory
from src.modules.todo_categories.service import TodoCategoriesService


async def provide_todo_categories_service(
    db_session: DBSessionDep,
) -> TodoCategoriesService:
    return TodoCategoriesService(db_session)


async def valid_todo_category_id(
    todo_category_id: int,
    service: Annotated[TodoCategoriesService, Depends(provide_todo_categories_service)],
) -> TodoCategory:
    if not (result := await service.get(todo_category_id)):
        raise TodoCategoryNotFound(todo_category_id, loc=("path", "id"))
    return result
