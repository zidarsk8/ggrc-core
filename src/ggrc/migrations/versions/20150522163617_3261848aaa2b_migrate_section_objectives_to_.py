# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

"""Migrate section_objectives to relationships

Revision ID: 3261848aaa2b
Revises: 5345a09722f1
Create Date: 2015-05-22 16:36:17.916138

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = '3261848aaa2b'
down_revision = '5345a09722f1'


def upgrade():
  sql = """
  REPLACE INTO relationships (
      modified_by_id, created_at, updated_at, source_id,
      source_type, destination_id, destination_type, context_id
  )
  SELECT so.modified_by_id, so.created_at, so.updated_at,
         so.section_id as source_id, s.type as source_type,
         so.objective_id as destination_id, "Objective" as destination_type,
         so.context_id
  FROM section_objectives as so JOIN sections as s ON so.section_id = s.id;
  """
  op.execute(sql)
  op.drop_constraint(
      'section_objectives_ibfk_1', 'section_objectives', type_='foreignkey')
  op.drop_constraint(
      'section_objectives_ibfk_2', 'section_objectives', type_='foreignkey')
  op.drop_constraint(
      'section_objectives_ibfk_3', 'section_objectives', type_='foreignkey')


def downgrade():
  op.create_foreign_key(
      'section_objectives_ibfk_1',
      'section_objectives',
      'contexts',
      ['context_id'],
      ['id']
  )
  op.create_foreign_key(
      'section_objectives_ibfk_2',
      'section_objectives',
      'objectives',
      ['objective_id'],
      ['id']
  )
  op.create_foreign_key(
      'section_objectives_ibfk_3',
      'section_objectives',
      'sections',
      ['section_id'],
      ['id']
  )
