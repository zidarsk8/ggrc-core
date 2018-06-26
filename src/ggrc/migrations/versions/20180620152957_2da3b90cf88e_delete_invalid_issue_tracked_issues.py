# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Delete invalid issue tracked issues

Create Date: 2018-06-20 15:29:57.068930
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

from alembic import op

# revision identifiers, used by Alembic.
revision = '2da3b90cf88e'
down_revision = '9bc9e8064e04'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  sql = """
    DELETE FROM issuetracker_issues
    WHERE object_id = 0 and object_type = "Audit"
  """
  op.execute(sql)


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
