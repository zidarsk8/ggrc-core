# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""System editable object state

Revision ID: 5254f4f31427
Revises: 512c71e4d93b
Create Date: 2015-02-05 02:05:09.351265

"""

# revision identifiers, used by Alembic.
revision = '5254f4f31427'
down_revision = '512c71e4d93b'

import sqlalchemy as sa
from sqlalchemy.sql import table, column
from alembic import op
from ggrc.models.track_object_state import ObjectStates, ObjectStateTables

def upgrade():
  for table_name in ObjectStateTables.table_names:
    op.add_column(table_name, sa.Column('os_state', sa.String(length=16), nullable=True))

    # Set the value into all existing records
    object_table = table(table_name,
                         column('os_state', sa.String(length=16)))
    connection = op.get_bind()
    connection.execute(
      object_table.update().values(
        {
          'os_state': ObjectStates.DRAFT
        }
      )
    )

    # Make the field not-nullable
    op.alter_column(table_name, 'os_state',existing_type=sa.String(length=16),nullable=False)

def downgrade():
  for table_name in ObjectStateTables.table_names:
    op.drop_column(table_name, 'os_state')
