# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Add Foreign key Snapshot - Audit

Delete snapshots that doesn't have correct parent_id or parent_type
Create foreign key for linking snapshots.parent_id and audits.id
Create Date: 2018-07-06 14:08:27.860421
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

from alembic import op

# revision identifiers, used by Alembic.
revision = '0e40a37a05f4'
down_revision = '054d15be7a29'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  op.execute(
      """
      DELETE FROM snapshots
      WHERE id IN (
          SELECT id
          FROM (
              SELECT s.id as id
              FROM snapshots as s
              LEFT JOIN audits as a
              ON s.parent_id = a.id
              WHERE a.id IS null OR s.parent_type != "Audit"
          ) sq
      );
      """
  )
  op.create_foreign_key(
      'fk_snapshots_audits',
      'snapshots',
      'audits',
      ['parent_id'],
      ['id'],
      ondelete="CASCADE",
  )


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  op.drop_constraint('fk_snapshots_audits', 'snapshots', type_='foreignkey')
  op.drop_index('fk_snapshots_audits', table_name='snapshots')
