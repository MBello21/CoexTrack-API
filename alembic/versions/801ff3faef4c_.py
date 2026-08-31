"""empty message

Revision ID: 801ff3faef4c
Revises: 052fb45252cf
Create Date: 2026-08-31 11:18:17.538001

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '801ff3faef4c'
down_revision: Union[str, Sequence[str], None] = '052fb45252cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('vehicles', sa.Column(
        'last_address', sa.String(255), nullable=True))


def downgrade() -> None:
    op.drop_column('vehicles', 'last_address')
