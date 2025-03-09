"""Add a column

Revision ID: 1d7825a978c0
Revises: 9c4bdca09317
Create Date: 2025-03-01 10:27:28.481231

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d7825a978c0'
down_revision: Union[str, None] = '9c4bdca09317'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
