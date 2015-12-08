# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""add enabled flag to person

Revision ID: 3a4ce23d81b0
Revises: 53bb0f4f6ec8
Create Date: 2014-09-17 20:44:20.246783
  
"""

# revision identifiers, used by Alembic.
revision = '3a4ce23d81b0'
down_revision = '53bb0f4f6ec8'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text

def upgrade():
  op.add_column('people', sa.Column('is_enabled', sa.Boolean()))
  conn = op.get_bind()
  op.execute(text("""update people set is_enabled=1 where 1=1"""))
  op.alter_column('people', 'is_enabled', existing_type=sa.Boolean(), nullable=False)

def downgrade():
  op.drop_column('people', 'is_enabled')
