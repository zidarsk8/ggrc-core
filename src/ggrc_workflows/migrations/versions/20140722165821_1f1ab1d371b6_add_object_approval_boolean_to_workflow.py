
"""Add object approval boolean to workflow

Revision ID: 1f1ab1d371b6
Revises: 19a67dc67c3
Create Date: 2014-07-22 16:58:21.242051

"""

# revision identifiers, used by Alembic.
revision = '1f1ab1d371b6'
down_revision = '19a67dc67c3'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.add_column('workflows', sa.Column('object_approval', sa.Boolean(), nullable=False))


def downgrade():
    op.drop_column('workflows', 'object_approval')
