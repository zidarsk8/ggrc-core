# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

"""Migrate directive_sections to relationships

Revision ID: 324d461206
Revises: a2fc29a71f3
Create Date: 2015-05-21 12:50:08.987209

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = '324d461206'
down_revision = 'a2fc29a71f3'

def upgrade():
  sql = """
  REPLACE INTO relationships (
      modified_by_id, created_at, updated_at, source_id,
      source_type, destination_id, destination_type, context_id
  )
  SELECT dc.modified_by_id, dc.created_at, dc.updated_at,
         dc.section_id as source_id, 'Clause' as source_type,
         dc.directive_id as destination_id,
         d.meta_kind as destination_type,
         dc.context_id
  FROM directive_sections as dc JOIN directives as d ON dc.directive_id = d.id;
  """
  op.execute(sql)
  op.drop_constraint(
      'directive_sections_ibfk_1',
      'directive_sections',
      type_='foreignkey')
  op.drop_constraint(
      'directive_sections_ibfk_2',
      'directive_sections',
      type_='foreignkey')
  op.drop_constraint(
      'directive_sections_ibfk_3',
      'directive_sections',
      type_='foreignkey')


def downgrade():
  op.create_foreign_key(
      'directive_sections_ibfk_1',
      'directive_sections',
      'contexts',
      ['context_id'],
      ['id'])
  op.create_foreign_key(
      'directive_sections_ibfk_2',
      'directive_sections',
      'sections',
      ['section_id'],
      ['id'])
  op.create_foreign_key(
      'directive_sections_ibfk_3',
      'directive_sections',
      'directives',
      ['directive_id'],
      ['id'])
