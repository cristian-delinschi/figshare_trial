"""Create accounts table

Revision ID: e96544824241
Revises: 
Create Date: 2024-08-24 11:40:13.633994

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'e96544824241'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

from sqlalchemy.sql import func


def upgrade() -> None:
    op.create_table(
        'accounts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), index=True),
        sa.Column('created_date', sa.DateTime(), server_default=func.now(), nullable=False),
        sa.Column('last_login_date', sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('accounts')
