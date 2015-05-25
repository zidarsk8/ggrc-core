# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

"""Migrate object_controls to relationships

Revision ID: 29d21b3c24b4
Revises: b0c3361797a
Create Date: 2015-05-21 09:16:09.620314

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = '29d21b3c24b4'
down_revision = 'b0c3361797a'


def upgrade():
  sql = """
  REPLACE INTO relationships (
      modified_by_id, created_at, updated_at, source_id,
      source_type, destination_id, destination_type, context_id
  )
  SELECT modified_by_id, created_at, updated_at, control_id as source_id,
         'Control' as source_type, controllable_id as destination_id,
         controllable_type as destination_type, context_id
  FROM object_controls;
  """
  op.execute(sql)
  op.drop_constraint(
      'object_controls_ibfk_1', 'object_controls', type_='foreignkey')
  op.drop_constraint(
      'object_controls_ibfk_2', 'object_controls', type_='foreignkey')


def downgrade():
  op.create_foreign_key(
      'object_controls_ibfk_1',
      'object_controls',
      'contexts',
      ['context_id'],
      ['id']
  )
  op.create_foreign_key(
      'object_controls_ibfk_2',
      'object_controls',
      'controls',
      ['control_id'],
      ['id']
  )
