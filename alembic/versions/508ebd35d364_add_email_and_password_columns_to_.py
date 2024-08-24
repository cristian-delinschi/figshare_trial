"""Add email and password columns to accounts

Revision ID: 508ebd35d364
Revises: e96544824241
Create Date: 2024-08-24 12:04:45.443817

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '508ebd35d364'
down_revision: Union[str, None] = 'e96544824241'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('accounts', sa.Column('email', sa.String(length=255), nullable=False, unique=True))
    op.add_column('accounts', sa.Column('password', sa.String(length=255), nullable=False))
    op.add_column('accounts', sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.false()))


def downgrade() -> None:
    op.drop_column('accounts', 'is_active')
    op.drop_column('accounts', 'password')
    op.drop_column('accounts', 'email')
