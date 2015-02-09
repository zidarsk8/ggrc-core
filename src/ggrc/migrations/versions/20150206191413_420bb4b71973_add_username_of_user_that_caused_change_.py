
"""Add username of user that caused change to object state

Revision ID: 420bb4b71973
Revises: 5254f4f31427
Create Date: 2015-02-06 19:14:13.884946

"""

# revision identifiers, used by Alembic.
revision = '420bb4b71973'
down_revision = '5254f4f31427'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from ggrc.models.track_object_state import ObjectStates, ObjectStateTables

def upgrade():
  for table_name in ObjectStateTables.table_names:
    op.add_column(table_name, sa.Column('os_last_updated_by_user_id', sa.Integer(), nullable=True))

def downgrade():
  for table_name in ObjectStateTables:
    op.drop_column(table_name, 'os_last_updated_by_user_id')
