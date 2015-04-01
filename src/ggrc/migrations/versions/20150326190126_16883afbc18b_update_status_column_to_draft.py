# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Update status column to draft

Revision ID: 16883afbc18b
Revises: 56bda17c92ee
Create Date: 2015-03-26 19:01:26.702662

"""

# revision identifiers, used by Alembic.
revision = '16883afbc18b'
down_revision = '56bda17c92ee'

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
