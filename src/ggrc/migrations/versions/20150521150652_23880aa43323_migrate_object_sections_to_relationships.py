# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

"""Migrate object_sections to relationships

Revision ID: 23880aa43323
Revises: 324d461206
Create Date: 2015-05-21 15:06:52.172183

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = '23880aa43323'
down_revision = '324d461206'


def upgrade():
  sql = """
  REPLACE INTO relationships (
      modified_by_id, created_at, updated_at, source_id,
      source_type, destination_id, destination_type, context_id
  )
  SELECT os.modified_by_id, os.created_at, os.updated_at,
         os.section_id as source_id, s.type as source_type,
         os.sectionable_id as destination_id,
         os.sectionable_type as destination_type, os.context_id
  FROM object_sections as os JOIN sections as s ON os.section_id = s.id;
  """
  op.execute(sql)
  op.drop_constraint(
      'object_sections_ibfk_1', 'object_sections', type_='foreignkey')
  op.drop_constraint(
      'object_sections_ibfk_2', 'object_sections', type_='foreignkey')


def downgrade():
  op.create_foreign_key(
      'object_sections_ibfk_1',
      'object_sections',
      'contexts',
      ['context_id'],
      ['id']
  )
  op.create_foreign_key(
      'object_sections_ibfk_2',
      'object_sections',
      'sections',
      ['section_id'],
      ['id']
  )
