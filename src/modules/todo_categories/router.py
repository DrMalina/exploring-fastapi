from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv
from sqlalchemy.exc import IntegrityError
from starlette import status

from src.exceptions import CustomValidationError
from src.modules.todo_categories.dependencies import set_up_todo_categories_service
from src.modules.todo_categories.schemas import TodoCategory, TodoCategoryCreate
from src.modules.todo_categories.service import TodoCategoriesService
from src.utils.db import is_unique_validation_integrity_error

router = APIRouter()


@cbv(router)
class TodoCategoriesRouter:
    _service: TodoCategoriesService = Depends(set_up_todo_categories_service)

    @router.post(
        "/", status_code=status.HTTP_201_CREATED, summary="Create a Todo Category"
    )
    async def create(self, todo_category: TodoCategoryCreate) -> TodoCategory:
        try:
            result = await self._service.create(todo_category)
            return TodoCategory.model_validate(result)
        except IntegrityError as ex:
            if is_unique_validation_integrity_error(ex):
                raise CustomValidationError(
                    title=TodoCategory.__name__,
                    error_type="unique",
                    msg="A Todo Category with that name already exists.",
                    loc=("body", "name"),
                    input_value=todo_category.name,
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
