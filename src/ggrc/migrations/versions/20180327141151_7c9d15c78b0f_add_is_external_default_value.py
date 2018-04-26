# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
add is_external default value

Create Date: 2018-03-27 14:11:51.923110
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = '7c9d15c78b0f'
down_revision = '48a49f384b2e'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  op.alter_column(
      "relationships",
      "is_external",
      nullable=False,
      server_default=sa.false(),
      existing_type=sa.Boolean,
  )


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  op.alter_column(
      "relationships",
      "is_external",
      nullable=False,
      server_default=None,
      existing_type=sa.Boolean,
  )
