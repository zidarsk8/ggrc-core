# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jost@reciprocitylabs.com
# Maintained By: jost@reciprocitylabs.com

"""Make task_group_task_id nullable on cycle task

Revision ID: 38af92d913dc
Revises: 1263c1ab4642
Create Date: 2016-04-05 16:15:33.917631

"""

# revision identifiers, used by Alembic.
revision = '38af92d913dc'
down_revision = '1263c1ab4642'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.alter_column('cycle_task_group_object_tasks', 'task_group_task_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)

def downgrade():
    op.alter_column('cycle_task_group_object_tasks', 'task_group_task_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    # TODO: make a default to something, currently it defaults to 0, app might break
    # maybe use this 0 as equal to null