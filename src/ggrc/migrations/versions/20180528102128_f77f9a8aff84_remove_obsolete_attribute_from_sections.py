# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Remove obsolete attribute from sections

Create Date: 2018-05-28 10:21:28.724134
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from alembic import op

# revision identifiers, used by Alembic.
revision = 'f77f9a8aff84'
down_revision = '5d0fa1d7d55d'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  op.drop_column('sections', 'na')


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  op.add_column(
      'sections',
      sa.Column(
          'na',
          mysql.TINYINT(display_width=1),
          autoincrement=False,
          nullable=False
      )
  )
