# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

"""Migrate program_directives to relationships

Revision ID: 3be12e136921
Revises: 41bd73114fd9
Create Date: 2015-04-28 15:23:10.503624

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = '3be12e136921'
down_revision = '41bd73114fd9'


def upgrade():
  sql = """
  REPLACE INTO relationships (
      modified_by_id, created_at, updated_at, source_id,
      source_type, destination_id, destination_type, context_id
  )
  SELECT pd.modified_by_id, pd.created_at, pd.updated_at, pd.program_id as source_id,
         'Program' as source_type, pd.directive_id, d.meta_kind as destination_type, pd.context_id
  FROM program_directives as pd JOIN directives as d ON pd.directive_id = d.id;
  """
  op.execute(sql)
  op.drop_constraint('fk_program_directives_contexts', 'program_directives', type_='foreignkey')
  op.drop_constraint('program_directives_ibfk_1', 'program_directives', type_='foreignkey')
  op.drop_constraint('program_directives_ibfk_2', 'program_directives', type_='foreignkey')


def downgrade():
  op.create_foreign_key('fk_program_directives_contexts', 'program_directives', 'contexts', ['context_id'], ['id'])
  op.create_foreign_key('program_directives_ibfk_1', 'program_directives', 'directives', ['directive_id'], ['id'])
  op.create_foreign_key('program_directives_ibfk_2', 'program_directives', 'programs', ['program_id'], ['id'])
