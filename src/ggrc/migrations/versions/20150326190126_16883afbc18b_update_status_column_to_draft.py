# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Update status column to draft

Revision ID: 5180ce718082
Revises: 1019280358f0
Create Date: 2015-04-02 15:56:09.861162

"""

# revision identifiers, used by Alembic.
revision = '5180ce718082'
down_revision = '1019280358f0'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from ggrc.models.track_object_state import ObjectStates, ObjectStateTables

def upgrade():
  for table_name in ObjectStateTables.table_names:
    # Set the status value to Draft in all existing records where the value is Null
    object_table = table(table_name, column('status', sa.String(length=250)))

    op.execute(
      object_table.update().values(status = ObjectStates.DRAFT)\
        .where(object_table.c.status == None)
    )


def downgrade():
  pass
