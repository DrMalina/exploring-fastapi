from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class TodoCategory(Base):
    __tablename__ = "todo_categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"<TodoCategory(id={self.id!r}, name={self.name!r})>"
