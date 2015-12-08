# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

"""Migrate control_sections to relationships

Revision ID: b0c3361797a
Revises: 32e064034091
Create Date: 2015-05-20 10:35:39.561584

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = 'b0c3361797a'
down_revision = '32e064034091'


def upgrade():
  sql = """
  REPLACE INTO relationships (
      modified_by_id, created_at, updated_at, source_id,
      source_type, destination_id, destination_type, context_id
  )
  SELECT modified_by_id, created_at, updated_at, control_id as source_id,
         'Control' as source_type, section_id as destination_id,
         'Section' as destination_type, context_id
  FROM control_sections;
  """
  op.execute(sql)
  op.drop_constraint(
      'fk_control_sections_contexts', 'control_sections', type_='foreignkey')
  op.drop_constraint(
      'control_sections_ibfk_1', 'control_sections', type_='foreignkey')
  op.drop_constraint(
      'control_sections_ibfk_2', 'control_sections', type_='foreignkey')


def downgrade():
  op.create_foreign_key(
      'fk_control_sections_contexts',
      'control_sections',
      'contexts',
      ['context_id'],
      ['id']
  )
  op.create_foreign_key(
      'control_sections_ibfk_1',
      'control_sections',
      'controls',
      ['control_id'],
      ['id']
  )
  op.create_foreign_key(
      'control_controls_ibfk_2',
      'control_sections',
      'sections',
      ['section_id'],
      ['id']
  )
