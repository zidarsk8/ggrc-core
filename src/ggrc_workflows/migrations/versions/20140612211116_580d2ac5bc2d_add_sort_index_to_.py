# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""Add sort_index to CycleTaskGroupObjectTask

Revision ID: 580d2ac5bc2d
Revises: 5ac75b9cbb64
Create Date: 2014-06-12 21:11:16.736323

"""

# revision identifiers, used by Alembic.
revision = '580d2ac5bc2d'
down_revision = '5ac75b9cbb64'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('cycle_task_group_object_tasks', sa.Column('sort_index', sa.String(length=250), nullable=False))


def downgrade():
    op.drop_column('cycle_task_group_object_tasks', 'sort_index')
