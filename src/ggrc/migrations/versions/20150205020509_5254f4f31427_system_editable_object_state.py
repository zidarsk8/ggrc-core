
"""System editable object state

Revision ID: 5254f4f31427
Revises: 512c71e4d93b
Create Date: 2015-02-05 02:05:09.351265

"""

# revision identifiers, used by Alembic.
revision = '5254f4f31427'
down_revision = '512c71e4d93b'

from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.sql import table, column
from alembic import op
from ggrc.models.track_object_state import ObjectStates, ObjectStateTables

def upgrade():
  for table_name in ObjectStateTables.table_names:
    op.add_column(table_name, sa.Column('os_state', sa.String(length=16), nullable=True))
    op.add_column(table_name, sa.Column('os_last_updated', sa.DateTime(), nullable=True))
    op.add_column(table_name, sa.Column('os_approved_on', sa.DateTime(), nullable=True))

    # Set the value into all existing records
    object_table = table(table_name,
                         column('os_state', sa.String(length=16)),
                         column('os_last_updated', sa.DATETIME))
    now = datetime.now()
    connection = op.get_bind()
    connection.execute(
      object_table.update().values(
        {
          'os_state': ObjectStates.DRAFT,
          'os_last_updated': now
        }
      )
    )

    # Make the field not-nullable
    op.alter_column(table_name, 'os_state',existing_type=sa.String(length=16),nullable=False)
    op.alter_column(table_name, 'os_last_updated',existing_type=sa.DateTime(),nullable=False)

def downgrade():
  for table_name in ObjectStateTables:
    op.drop_column(table_name, 'os_state')
    op.drop_column(table_name, 'os_last_updated')
    op.drop_column(table_name, 'os_approved_on')
