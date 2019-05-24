# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Add filters column to saved_searches model

Create Date: 2019-05-24 12:17:53.909305
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = '6bac46a8d3e7'
down_revision = '296bde07a661'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  op.add_column(
      'saved_searches',
      sa.Column('filters', sa.Text, nullable=True),
  )


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  op.drop_column('saved_searches', 'filters')
