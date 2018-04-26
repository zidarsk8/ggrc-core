# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Add relationship to proposals

Create Date: 2018-04-19 10:22:58.289500
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

from alembic import op


# revision identifiers, used by Alembic.
revision = 'fcd5e64ff664'
down_revision = '082306b17b07'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  op.execute("""
      INSERT INTO relationships(
          source_type,
          source_id,
          destination_type,
          destination_id,
          created_at,
          updated_at,
          is_external
      )
      SELECT instance_type, instance_id, 'Proposal', id, NOW(), NOW(), '0'
      FROM proposals;
  """)


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  op.execute("""
      DELETE FROM relationships
      WHERE source_type = 'Proposal' OR destination_type = 'Proposal';
  """)
