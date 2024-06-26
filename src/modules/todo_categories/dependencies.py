from src.dependencies import DBSessionDep
from src.modules.todo_categories.service import TodoCategoriesService


def set_up_todo_categories_service(db_session: DBSessionDep) -> TodoCategoriesService:
    return TodoCategoriesService(db_session)
