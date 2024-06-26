from fastapi import APIRouter

from src.modules.todo_categories.router import router as todo_categories_router

api_router = APIRouter()

api_router.include_router(todo_categories_router,
                          prefix="/todo-categories", tags=["TodoCategories"])
