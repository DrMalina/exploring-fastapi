from src.dependencies import DBSessionDep
from src.modules.todos.service import TodoService


async def provide_todo_service(
    db_session: DBSessionDep,
) -> TodoService:
    return TodoService(db_session)
