# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Remove Meeting

Create Date: 2017-09-08 14:12:55.361026
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4bb6fa8fb5e1'
down_revision = '5405cc1ae721'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  op.drop_table('object_events')
  op.drop_table('meetings')


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  op.create_table('meetings',
                  sa.Column('id', mysql.INTEGER(display_width=11),
                            nullable=False),
                  sa.Column('title', mysql.VARCHAR(length=250),
                            nullable=False),
                  sa.Column('created_at', mysql.DATETIME(), nullable=False),
                  sa.Column('modified_by_id', mysql.INTEGER(display_width=11),
                            autoincrement=False, nullable=True),
                  sa.Column('updated_at', mysql.DATETIME(), nullable=False),
                  sa.Column('context_id', mysql.INTEGER(display_width=11),
                            autoincrement=False, nullable=True),
                  sa.Column('description', mysql.TEXT(), nullable=True),
                  sa.Column('start_at', mysql.DATETIME(), nullable=False),
                  sa.Column('end_at', mysql.DATETIME(), nullable=False),
                  sa.ForeignKeyConstraint(['context_id'], [u'contexts.id'],
                                          name=u'meetings_ibfk_1'),
                  sa.PrimaryKeyConstraint('id'),
                  mysql_default_charset=u'utf8',
                  mysql_engine=u'InnoDB')
  op.create_table('object_events',
                  sa.Column('id', mysql.INTEGER(display_width=11),
                            nullable=False),
                  sa.Column('modified_by_id', mysql.INTEGER(display_width=11),
                            autoincrement=False, nullable=True),
                  sa.Column('created_at', mysql.DATETIME(), nullable=False),
                  sa.Column('updated_at', mysql.DATETIME(), nullable=False),
                  sa.Column('context_id', mysql.INTEGER(display_width=11),
                            autoincrement=False, nullable=True),
                  sa.Column('calendar_id', mysql.VARCHAR(length=250),
                            nullable=True),
                  sa.Column('event_id', mysql.VARCHAR(length=250),
                            nullable=False),
                  sa.Column('eventable_id', mysql.INTEGER(display_width=11),
                            autoincrement=False, nullable=False),
                  sa.Column('eventable_type', mysql.VARCHAR(length=250),
                            nullable=False),
                  sa.PrimaryKeyConstraint('id'),
                  mysql_default_charset=u'utf8',
                  mysql_engine=u'InnoDB')
