# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

"""Migrate program_controls to relationships

Revision ID: 303ebb722f41
Revises: 3be12e136921
Create Date: 2015-04-29 13:23:34.420607

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = '303ebb722f41'
down_revision = '3be12e136921'


def upgrade():
  sql = """
  REPLACE INTO relationships (
      modified_by_id, created_at, updated_at, source_id,
      source_type, destination_id, destination_type, context_id
  )
  SELECT modified_by_id, created_at, updated_at, program_id as source_id,
         'Program' as source_type, control_id as destination_id, 'Control' as destination_type, context_id
  FROM program_controls;
  """
  op.execute(sql)
  op.drop_constraint('fk_program_controls_control', 'program_controls', type_='foreignkey')
  op.drop_constraint('fk_program_controls_program', 'program_controls', type_='foreignkey')


def downgrade():
  op.create_foreign_key('fk_program_controls_control', 'program_controls', 'controls', ['control_id'], ['id'])
  op.create_foreign_key('fk_program_controls_program', 'program_controls', 'programs', ['program_id'], ['id'])
