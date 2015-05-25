# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

"""Migrate directive_controls to relationships

Revision ID: a2fc29a71f3
Revises: 29d21b3c24b4
Create Date: 2015-05-21 10:21:27.522517

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = 'a2fc29a71f3'
down_revision = '29d21b3c24b4'


def upgrade():
  sql = """
  REPLACE INTO relationships (
      modified_by_id, created_at, updated_at, source_id,
      source_type, destination_id, destination_type, context_id
  )
  SELECT dc.modified_by_id, dc.created_at, dc.updated_at,
         dc.control_id as source_id, 'Control' as source_type,
         dc.directive_id as destination_id,
         d.meta_kind as destination_type,
         dc.context_id
  FROM directive_controls as dc JOIN directives as d ON dc.directive_id = d.id;
  """
  op.execute(sql)
  op.drop_constraint(
      'fk_context_id',
      'directive_controls',
      type_='foreignkey')
  op.drop_constraint(
      'fk_control_id',
      'directive_controls',
      type_='foreignkey')
  op.drop_constraint(
      'fk_directive_id',
      'directive_controls',
      type_='foreignkey')


def downgrade():
  op.create_foreign_key(
      'fk_context_id',
      'directive_controls',
      'contexts',
      ['context_id'],
      ['id']
  )
  op.create_foreign_key(
      'fk_control_id',
      'directive_controls',
      'controls',
      ['control_id'],
      ['id'])
  op.create_foreign_key(
      'fk_directive_id',
      'directive_controls',
      'directives',
      ['directive_id'],
      ['id'])
