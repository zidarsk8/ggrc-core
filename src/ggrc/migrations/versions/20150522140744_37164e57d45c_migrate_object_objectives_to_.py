# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

"""Migrate object_objectives to relationships

Revision ID: 37164e57d45c
Revises: 23880aa43323
Create Date: 2015-05-22 14:07:44.687449

"""

# revision identifiers, used by Alembic.
revision = '37164e57d45c'
down_revision = '23880aa43323'

from alembic import op


def upgrade():
  sql = """
  REPLACE INTO relationships (
      modified_by_id, created_at, updated_at, source_id,
      source_type, destination_id, destination_type, context_id
  )
  SELECT modified_by_id, created_at, updated_at,
         objective_id as source_id, "Objective" as source_type,
         objectiveable_id as destination_id,
         objectiveable_type as destination_type, context_id
  FROM object_objectives;
  """
  op.execute(sql)
  op.drop_constraint(
      'object_objectives_ibfk_1', 'object_objectives', type_='foreignkey')
  op.drop_constraint(
      'object_objectives_ibfk_2', 'object_objectives', type_='foreignkey')


def downgrade():
  op.create_foreign_key(
      'object_objectives_ibfk_1',
      'object_objectives',
      'contexts',
      ['context_id'],
      ['id']
  )
  op.create_foreign_key(
      'object_objectives_ibfk_2',
      'object_objectives',
      'objectives',
      ['objective_id'],
      ['id']
  )
