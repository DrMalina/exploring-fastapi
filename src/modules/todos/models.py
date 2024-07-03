from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base
from src.db.mixin import TimestampMixin

if TYPE_CHECKING:
    from src.modules.todo_categories.models import TodoCategory


class Todo(TimestampMixin, Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    is_completed: Mapped[bool] = mapped_column(default=False)

    todo_category_id: Mapped[int] = mapped_column(ForeignKey("todo_categories.id"))
    todo_category: Mapped["TodoCategory"] = relationship(
        "TodoCategory", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Todo(id={self.id!r}, name={self.name!r})>"
