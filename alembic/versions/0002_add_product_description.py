"""add description to products

Revision ID: 0002_add_product_description
Revises: 0001_create_products
Create Date: 2026-05-15
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0002_add_product_description"
down_revision: Union[str, None] = "0001_create_products"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # server_default нужен, чтобы SQLite смог добавить NOT NULL колонку,
    # если в таблице уже есть записи.
    op.add_column(
        "products",
        sa.Column("description", sa.String(length=255), nullable=False, server_default="No description"),
    )


def downgrade() -> None:
    op.drop_column("products", "description")
