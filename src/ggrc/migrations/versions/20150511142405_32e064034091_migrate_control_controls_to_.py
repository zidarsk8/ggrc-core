# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

"""Migrate control_controls to relationships

Revision ID: 32e064034091
Revises: 303ebb722f41
Create Date: 2015-05-11 14:24:05.711598

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = '32e064034091'
down_revision = '303ebb722f41'


def upgrade():
  sql = """
  REPLACE INTO relationships (
      modified_by_id, created_at, updated_at, source_id,
      source_type, destination_id, destination_type, context_id
  )
  SELECT modified_by_id, created_at, updated_at, control_id as source_id,
         'Control' as source_type, implemented_control_id as destination_id,
         'Control' as destination_type, context_id
  FROM control_controls;
  """
  op.execute(sql)
  op.drop_constraint(
      'fk_control_controls_contexts', 'control_controls', type_='foreignkey')
  op.drop_constraint(
      'control_controls_ibfk_1', 'control_controls', type_='foreignkey')
  op.drop_constraint(
      'control_controls_ibfk_2', 'control_controls', type_='foreignkey')


def downgrade():
  op.create_foreign_key(
      'fk_control_controls_contexts',
      'control_controls',
      'contexts',
      ['context_id'],
      ['id']
  )
  op.create_foreign_key(
      'control_controls_ibfk_1',
      'control_controls',
      'controls',
      ['control_id'],
      ['id']
  )
  op.create_foreign_key(
      'control_controls_ibfk_2',
      'control_controls',
      'controls',
      ['implemented_control_id'],
      ['id']
  )
