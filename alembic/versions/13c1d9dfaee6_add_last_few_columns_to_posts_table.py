"""add last few columns to posts table

Revision ID: 13c1d9dfaee6
Revises: f1e0cc578e03
Create Date: 2024-01-17 00:42:05.659715

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '13c1d9dfaee6'
down_revision: Union[str, None] = 'f1e0cc578e03'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default= 'TRUE'),) 
    op.add_column('posts', sa.Column( 'created_at', sa.TIMESTAMP(timezone=True), nullable= False, server_defaut= sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts','created_at')
    pass
