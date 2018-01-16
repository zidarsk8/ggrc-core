# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
object_folders table became unused when folder field was added to the
'programs', 'audits', 'controls'

This is just a clean up after the migration to folder fields.

Create Date: 2017-12-28 09:12:47.822789
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = '3f64d03c6c01'
down_revision = '4491d7eaca49'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  op.drop_table('object_folders')


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  op.create_table(
      'object_folders',
      sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
      sa.Column('modified_by_id', sa.Integer()),
      sa.Column(
          'created_at', sa.DateTime(), default=sa.text('current_timestamp')),
      sa.Column(
          'updated_at',
          sa.DateTime(),
          default=sa.text('current_timestamp'),
          onupdate=sa.text('current_timestamp')),
      sa.Column('context_id', sa.Integer()),
      sa.Column('parent_folder_id', sa.String(length=250), nullable=True),
      sa.Column('folder_id', sa.String(length=250), nullable=False),
      sa.Column('folderable_id', sa.Integer(), nullable=False),
      sa.Column('folderable_type', sa.String(length=250), nullable=False),
  )
  op.create_index('ix_folderable_id_type', 'object_folders',
                  ['folderable_type', 'folderable_id'], unique=False)
  op.create_index('ix_object_folders_updated_at', 'object_folders',
                  ['updated_at', ], unique=False)
  op.create_index('fk_object_folders_contexts', 'object_folders',
                  ['context_id', ], unique=False)
