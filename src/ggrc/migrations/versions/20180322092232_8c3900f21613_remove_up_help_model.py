# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Remove up Help model

Create Date: 2018-03-22 09:22:32.697632
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import sqlalchemy as sa

from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8c3900f21613'
down_revision = '70fdda308cb7'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  op.drop_table('helps')


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  op.create_table(
      'helps',
      sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
      sa.Column('modified_by_id', mysql.INTEGER(display_width=11),
                autoincrement=False, nullable=True),
      sa.Column('created_at', mysql.DATETIME(), nullable=False),
      sa.Column('updated_at', mysql.DATETIME(), nullable=False),
      sa.Column('slug', mysql.VARCHAR(length=250), nullable=False),
      sa.Column('title', mysql.VARCHAR(length=250), nullable=False),
      sa.Column('content', mysql.TEXT(), nullable=False),
      sa.Column('context_id', mysql.INTEGER(display_width=11),
                autoincrement=False, nullable=True),
      sa.ForeignKeyConstraint(['context_id'], [u'contexts.id'],
                              name=u'fk_helps_contexts'),
      sa.PrimaryKeyConstraint('id'),
      mysql_default_charset=u'utf8',
      mysql_engine=u'InnoDB',
  )
