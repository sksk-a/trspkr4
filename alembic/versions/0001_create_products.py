"""create products table

Revision ID: 0001_create_products
Revises: None
Create Date: 2026-05-15
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001_create_products"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("count", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_index(op.f("ix_products_id"), "products", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_products_id"), table_name="products")
    op.drop_table("products")
