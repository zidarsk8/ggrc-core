
"""Add object_approval flag to taskgrouptask

Revision ID: c8263593153
Revises: 468290d5494f
Create Date: 2014-08-01 21:39:48.857784

"""

# revision identifiers, used by Alembic.
revision = 'c8263593153'
down_revision = '468290d5494f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
      'task_group_tasks',
      sa.Column('object_approval', sa.Boolean(), nullable=False))
    op.execute('update task_group_tasks tgt, task_groups tg, ' \
      + 'workflows wf, tasks ts set tgt.object_approval = true where ' \
      + 'tgt.task_group_id=tg.id and tg.workflow_id=wf.id and ' \
      + 'tgt.task_id=ts.id and ' \
      + "wf.object_approval=true and ts.title like 'Object review %'"
      )

def downgrade():
    op.drop_column('task_group_tasks', 'object_approval')

