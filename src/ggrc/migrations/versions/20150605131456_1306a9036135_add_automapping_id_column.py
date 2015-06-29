# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: andraz@reciprocitylabs.com
# Maintained By: andraz@reciprocitylabs.com

"""add automapping id column

Revision ID: 1306a9036135
Revises: 3261848aaa2b
Create Date: 2015-06-05 13:14:56.644865

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1306a9036135'
down_revision = '1d1e9807c46c'


def upgrade():
  op.add_column(
      'relationships',
      sa.Column('automapping_id', sa.Integer(), nullable=True)
  )
  op.create_foreign_key(
      'relationships_automapping_parent',
      'relationships',
      'relationships',
      ['automapping_id'],
      ['id'],
      ondelete='SET NULL'
  )


def downgrade():
  op.drop_constraint('relationships_automapping_parent', 'relationships',
                     type_='foreignkey')
  op.drop_column('relationships', 'automapping_id')
