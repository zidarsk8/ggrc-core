# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Remove ACL w/o corresponding documents

Create Date: 2018-06-13 13:25:24.380355
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

from alembic import op


# revision identifiers, used by Alembic.
revision = 'e1256da10630'
down_revision = '8ffc6d30dba2'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  op.execute("SET SESSION SQL_SAFE_UPDATES = 0")

  sql = """
      DELETE acl FROM access_control_list acl
      LEFT JOIN documents d ON
        d.id = acl.object_id
      WHERE
        object_type = "Document" AND d.id IS NULL
  """
  op.execute(sql)


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
