# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Remove context from events

Create Date: 2018-06-24 16:42:09.526220
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from alembic import op

# revision identifiers, used by Alembic.
revision = '7a8eaf2c9b75'
down_revision = '2bec1dfcaec0'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  op.drop_constraint(u'fk_events_contexts', 'events', type_='foreignkey')
  op.drop_column('events', 'context_id')


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  op.add_column(
      'events',
      sa.Column(
          'context_id',
          mysql.INTEGER(display_width=11),
          autoincrement=False,
          nullable=True,
      )
  )
  op.create_foreign_key(
      u'fk_events_contexts',
      'events',
      'contexts',
      ['context_id'],
      ['id'],
  )
