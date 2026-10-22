"""add product description

Revision ID: b35d2f0f74e7
Revises: ee388e92b086
Create Date: 2026-10-22 18:33:11.603274

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b35d2f0f74e7'
down_revision: Union[str, Sequence[str], None] = 'ee388e92b086'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "products",
        sa.Column(
            "description",
            sa.Text(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column(
        "products",
        "description",
    )
