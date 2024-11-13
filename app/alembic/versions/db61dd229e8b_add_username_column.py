"""Add username column

Revision ID: db61dd229e8b
Revises: 15488523d40e
Create Date: 2024-10-27 17:48:22.914693

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db61dd229e8b'
down_revision: Union[str, None] = '15488523d40e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('username', sa.String(length=200), unique=True, nullable=True))


def downgrade() -> None:
    pass
