# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""calendar_objects

Revision ID: e09d8acc49b
Revises: 1b9c6ce2ee00
Create Date: 2014-07-29 21:22:32.600380

"""

# revision identifiers, used by Alembic.
revision = 'e09d8acc49b'
down_revision = '1b9c6ce2ee00'

from alembic import op
import sqlalchemy as sa


def upgrade():
  op.create_table('calendar_entries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=True),
    sa.Column('calendar_id', sa.String(length=250), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_by_id', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('context_id', sa.Integer(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['context_id'], ['contexts.id'],),
    sa.ForeignKeyConstraint(['owner_id'], ['people.id'],),
    sa.PrimaryKeyConstraint('id')
  )

def downgrade():
  op.drop_table('calendar_entries')
