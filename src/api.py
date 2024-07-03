from fastapi import APIRouter

from src.modules.todo_categories.router import router as todo_categories_router
from src.modules.todos.router import router as todos_router

api_router = APIRouter()

api_router.include_router(
    todo_categories_router, prefix="/todo-categories", tags=["TodoCategories"]
)
api_router.include_router(todos_router, prefix="/todos", tags=["Todos"])
