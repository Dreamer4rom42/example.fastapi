"""add column to posts table

Revision ID: 00a37a17f73c
Revises: 459ef9f99178
Create Date: 2024-01-16 20:30:38.750279

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00a37a17f73c'
down_revision: Union[str, None] = '459ef9f99178'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("posts", sa.Column('content', sa.String(), nullable= False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
