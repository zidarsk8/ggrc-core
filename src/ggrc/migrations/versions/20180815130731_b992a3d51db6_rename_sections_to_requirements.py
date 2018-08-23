# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Rename sections to requirements in revisions

Create Date: 2018-08-15 13:07:31.681031
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

from alembic import op

# revision identifiers, used by Alembic.
revision = 'b992a3d51db6'
down_revision = '385ee48cd6b9'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  op.execute(
      """
          UPDATE `revisions`
          SET `destination_type` = "Requirement"
          WHERE `destination_type` = "Section"
      """
  )


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
