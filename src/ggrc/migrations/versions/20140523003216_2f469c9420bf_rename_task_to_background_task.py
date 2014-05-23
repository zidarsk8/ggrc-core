
"""Rename task to background_task

Revision ID: 2f469c9420bf
Revises: 51f6b61fd82a
Create Date: 2014-05-23 00:32:16.278242

"""

# revision identifiers, used by Alembic.
revision = '2f469c9420bf'
down_revision = '51f6b61fd82a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.rename_table('tasks', 'background_tasks')


def downgrade():
    op.rename_table('background_tasks', 'tasks')
