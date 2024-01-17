"""create posts table

Revision ID: 459ef9f99178
Revises: 
Create Date: 2024-01-16 13:23:40.727208

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '459ef9f99178'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts", sa.Column("id", sa.Integer(), nullable = False, primary_key= True), sa.Column("title", sa.String(), nullable= False))
    pass

def downgrade():
    op.drop_table("posts")
    pass

# str, Union[str, None] = None, Union[str, Sequence[str], None], Union[str,Sequence[str], None]