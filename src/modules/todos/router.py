from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv
from sqlalchemy.exc import IntegrityError
from starlette import status

from src.modules.todo_categories.exceptions import TodoCategoryNotFound
from src.modules.todos.dependencies import provide_todo_service
from src.modules.todos.schemas import Todo, TodoCreate
from src.modules.todos.service import TodoService
from src.utils.db import is_foreign_key_validation_integrity_error

router = APIRouter()


@cbv(router)
class TodosRouter:
    _service: TodoService = Depends(provide_todo_service)

    @router.post("/", status_code=status.HTTP_201_CREATED, summary="Create a Todo")
    async def create(self, todo: TodoCreate) -> Todo:
        try:
            result = await self._service.create(todo)
            return Todo.model_validate(result)
        except IntegrityError as ex:
            if is_foreign_key_validation_integrity_error(ex):
                raise TodoCategoryNotFound(
                    todo.todo_category_id, loc=("body", "todo_category_id")
                ) from ex
            raise

    @router.get("/", status_code=status.HTTP_200_OK, summary="Get all Todos")
    async def get_all(self) -> list[Todo]:
        return [Todo.model_validate(model) for model in await self._service.get_all()]
