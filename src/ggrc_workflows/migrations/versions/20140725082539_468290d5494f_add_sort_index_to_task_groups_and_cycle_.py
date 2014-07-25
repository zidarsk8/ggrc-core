
"""Add sort index to task_groups and cycle_task_groups

Revision ID: 468290d5494f
Revises: 4b3316aa1acf
Create Date: 2014-07-25 08:25:39.074611

"""

# revision identifiers, used by Alembic.
revision = '468290d5494f'
down_revision = '4b3316aa1acf'

from alembic import op
import sqlalchemy as sa


def upgrade():
  op.add_column('task_groups', sa.Column('sort_index', sa.String(length=250), nullable=False))
  op.add_column('cycle_task_groups', sa.Column('sort_index', sa.String(length=250), nullable=False))

def downgrade():
  op.drop_column('cycle_task_groups', 'sort_index')
  op.drop_column('task_groups', 'sort_index')
