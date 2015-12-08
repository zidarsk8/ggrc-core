# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

"""Migrate objective_controls to relationships

Revision ID: 5345a09722f1
Revises: 37164e57d45c
Create Date: 2015-05-22 14:54:52.747192

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = '5345a09722f1'
down_revision = '37164e57d45c'


def upgrade():
  sql = """
  REPLACE INTO relationships (
      modified_by_id, created_at, updated_at, source_id,
      source_type, destination_id, destination_type, context_id
  )
  SELECT modified_by_id, created_at, updated_at,
         objective_id as source_id, 'Objective' as source_type,
         control_id as destination_id, 'Control' as destination_type,
         context_id
  FROM objective_controls;
  """
  op.execute(sql)
  op.drop_constraint(
      'objective_controls_ibfk_1', 'objective_controls', type_='foreignkey')
  op.drop_constraint(
      'objective_controls_ibfk_2', 'objective_controls', type_='foreignkey')
  op.drop_constraint(
      'objective_controls_ibfk_3', 'objective_controls', type_='foreignkey')


def downgrade():
  op.create_foreign_key(
      'objective_controls_ibfk_1',
      'objective_controls',
      'contexts',
      ['context_id'],
      ['id']
  )
  op.create_foreign_key(
      'objective_controls_ibfk_2',
      'objective_controls',
      'controls',
      ['control_id'],
      ['id']
  )
  op.create_foreign_key(
      'objective_controls_ibfk_3',
      'objective_controls',
      'objectives',
      ['objective_id'],
      ['id']
  )
