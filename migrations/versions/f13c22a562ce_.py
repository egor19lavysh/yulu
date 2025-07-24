"""empty message

Revision ID: f13c22a562ce
Revises: 42d21f853d18
Create Date: 2025-07-24 20:37:49.348186

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f13c22a562ce'
down_revision: Union[str, Sequence[str], None] = '42d21f853d18'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
