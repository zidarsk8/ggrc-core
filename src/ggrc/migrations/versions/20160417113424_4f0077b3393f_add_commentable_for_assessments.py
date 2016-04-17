# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: peter@reciprocitylabs.com

"""Request comment notifications.

Create Date: 2016-03-21 11:07:07.327760
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '33459bd8b70d'
down_revision = '3914dbf78dc1'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  op.add_column(
      'assessments',
      sa.Column('recipients', sa.String(length=250), nullable=True)
  )
  op.add_column(
      'assessments',
      sa.Column('send_by_default', sa.Boolean(), nullable=True)
  )


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  op.drop_column('assessments', 'send_by_default')
  op.drop_column('assessments', 'recipients')
