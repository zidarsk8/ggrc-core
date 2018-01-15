# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Fix audit context on folders

Create Date: 2017-03-11 20:11:02.652252
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

from alembic import op


# revision identifiers, used by Alembic.
revision = '5405cc1ae721'
down_revision = '395186a2d8'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""

  # Clear object_folder
  sql = """
    UPDATE object_folders AS of
    JOIN audits AS au ON
      of.folderable_id = au.id AND
      of.folderable_type = "Audit"
    SET of.context_id = au.context_id
  """
  op.execute(sql)


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  pass
