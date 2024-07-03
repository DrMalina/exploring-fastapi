from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv
from sqlalchemy.exc import IntegrityError
from starlette import status

from src.modules.todo_categories.dependencies import (
    provide_todo_categories_service,
    valid_todo_category_id,
)
from src.modules.todo_categories.exceptions import (
    TodoCategoryAlreadyExists,
)
from src.modules.todo_categories.models import TodoCategory as TodoCategoryModel
from src.modules.todo_categories.schemas import TodoCategory, TodoCategoryCreate
from src.modules.todo_categories.service import TodoCategoriesService
from src.utils.db import is_unique_validation_integrity_error

router = APIRouter()


@cbv(router)
class TodoCategoriesRouter:
    _service: TodoCategoriesService = Depends(provide_todo_categories_service)

    @router.post(
        "/", status_code=status.HTTP_201_CREATED, summary="Create a Todo Category"
    )
    async def create(self, todo_category: TodoCategoryCreate) -> TodoCategory:
        try:
            result = await self._service.create(todo_category)
            return TodoCategory.model_validate(result)
        except IntegrityError as ex:
            if is_unique_validation_integrity_error(ex):
                raise TodoCategoryAlreadyExists(
                    todo_category.name, loc=("body", "name")
                ) from ex
            raise

    @router.get(
        "/", status_code=status.HTTP_200_OK, summary="Get a list of Todo Categories"
    )
    async def get_all(self) -> list[TodoCategory]:
        return [
            TodoCategory.model_validate(model)
            for model in await self._service.get_all()
        ]

    @router.get(
        "/{todo_category_id}",
        status_code=status.HTTP_200_OK,
        summary="Get Todo Category",
    )
    async def get(  # noqa: PLR6301
        self,
        todo_category: Annotated[TodoCategoryModel, Depends(valid_todo_category_id)],
    ) -> TodoCategory:
        return TodoCategory.model_validate(todo_category)
