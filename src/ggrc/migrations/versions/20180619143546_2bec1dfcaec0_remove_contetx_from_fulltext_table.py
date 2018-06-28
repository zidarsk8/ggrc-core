# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Remove contetx from fulltext table

Create Date: 2018-06-19 14:35:46.822517
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import sqlalchemy as sa

from sqlalchemy.dialects import mysql
from alembic import op

# revision identifiers, used by Alembic.
revision = '2bec1dfcaec0'
down_revision = '2da3b90cf88e'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  op.drop_index(
      'ix_fulltext_record_properties_context_id',
      table_name='fulltext_record_properties'
  )
  op.drop_column('fulltext_record_properties', 'context_id')


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  op.add_column(
      'fulltext_record_properties',
      sa.Column(
          'context_id',
          mysql.INTEGER(display_width=11),
          autoincrement=False,
          nullable=True
      )
  )
  op.create_index(
      'ix_fulltext_record_properties_context_id',
      'fulltext_record_properties',
      ['context_id'],
      unique=False
  )
