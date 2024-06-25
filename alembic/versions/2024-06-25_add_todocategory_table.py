"""add TodoCategory table

Revision ID: 775d0f9e1070
Revises: d6788368d4ad
Create Date: 2024-06-25 14:23:30.940814

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "775d0f9e1070"
down_revision: Union[str, None] = "d6788368d4ad"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "todo_categories",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(
        op.f("ix_todo_categories_id"), "todo_categories", ["id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_todo_categories_id"), table_name="todo_categories")
    op.drop_table("todo_categories")
    # ### end Alembic commands ###