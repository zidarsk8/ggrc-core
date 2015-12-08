# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

"""create object type table

Revision ID: 49541e2c6db5
Revises: 4dd6fbbc31fa
Create Date: 2015-04-01 15:57:24.004587

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '49541e2c6db5'
down_revision = '4dd6fbbc31fa'


def upgrade():
  object_types_table = op.create_table(
      'object_types',
      sa.Column('id', sa.Integer(), nullable=False),
      sa.Column('name', sa.String(length=250), nullable=False),
      sa.Column('description', sa.String(length=250), nullable=True),
      sa.Column('created_at', sa.DateTime(), nullable=True),
      sa.Column('modified_by_id', sa.Integer(), nullable=True),
      sa.Column('updated_at', sa.DateTime(), nullable=True),
      sa.Column('context_id', sa.Integer(), nullable=True),
      sa.PrimaryKeyConstraint('id')
  )
  op.create_index('object_types_name', 'object_types', ['name'], unique=True)


def downgrade():
  op.drop_table('object_types')
