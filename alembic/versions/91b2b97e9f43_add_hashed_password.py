"""Add hashed password

Revision ID: 91b2b97e9f43
Revises: 508ebd35d364
Create Date: 2024-08-24 14:25:35.346807

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '91b2b97e9f43'
down_revision: Union[str, None] = '508ebd35d364'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('accounts', sa.Column('hashed_password', sa.String(length=255), nullable=False))



def downgrade() -> None:
    op.drop_column('accounts', 'hashed_password')

