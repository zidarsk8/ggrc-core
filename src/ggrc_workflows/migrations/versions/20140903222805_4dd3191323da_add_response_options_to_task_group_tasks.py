
"""Add response options to task group tasks

Revision ID: 4dd3191323da
Revises: 23f5b46fc4a3
Create Date: 2014-09-03 22:28:05.079477

"""

# revision identifiers, used by Alembic.
revision = '4dd3191323da'
down_revision = '23f5b46fc4a3'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.add_column('cycle_task_group_object_tasks', sa.Column('response_options', sa.Text(), default="[]", nullable=False))
    op.add_column('cycle_task_group_object_tasks', sa.Column('selected_response_options', sa.Text(), default="[]", nullable=False))
    op.add_column('cycle_task_group_object_tasks', sa.Column('task_type', sa.String(length=250), nullable=False))
    op.add_column('task_group_tasks', sa.Column('response_options', sa.Text(), default="[]", nullable=False))
    op.add_column('task_group_tasks', sa.Column('task_type', sa.String(length=250), nullable=False))


def downgrade():
    op.drop_column('task_group_tasks', 'task_type')
    op.drop_column('task_group_tasks', 'response_options')
    op.drop_column('cycle_task_group_object_tasks', 'task_type')
    op.drop_column('cycle_task_group_object_tasks', 'selected_response_options')
    op.drop_column('cycle_task_group_object_tasks', 'response_options')
