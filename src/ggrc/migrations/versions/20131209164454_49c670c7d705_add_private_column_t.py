# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""Add private column to programs table.

Revision ID: 49c670c7d705
Revises: a3afeab3302
Create Date: 2013-12-09 16:44:54.222398

"""

# revision identifiers, used by Alembic.
revision = '49c670c7d705'
down_revision = 'a3afeab3302'

from alembic import op
from sqlalchemy.sql import table, column
import sqlalchemy as sa

def upgrade():
  op.add_column(
      'programs',
      sa.Column('private', sa.Boolean(), default=False, nullable=False),
      )
  programs_table = table('programs',
      column('id', sa.Integer),
      column('context_id', sa.Integer),
      column('private', sa.Boolean),
      )
  op.execute(programs_table.update().values(private=True)\
      .where(programs_table.c.context_id != None))
  
def downgrade():
  op.drop_column('programs', 'private')
