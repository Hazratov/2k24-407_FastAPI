"""create account table

Revision ID: 9c4bdca09317
Revises: 2931f15e7b5f
Create Date: 2025-03-01 10:26:23.150508

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c4bdca09317'
down_revision: Union[str, None] = '2931f15e7b5f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
