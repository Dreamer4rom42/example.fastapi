"""add foreign key to posts table

Revision ID: f1e0cc578e03
Revises: a0d4a60faad4
Create Date: 2024-01-17 00:14:51.571308

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1e0cc578e03'
down_revision: Union[str, None] = 'a0d4a60faad4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table= "posts", referent_table= 'users', local_cols= ['owner_id'], remote_cols= ['id'], ondelete= 'CASCADE')
    pass


def downgrade():
    op.drop_constraint('posts_users_fk', table_name= 'posts')
    op.drop_column('posts', 'owner_id')
    pass
