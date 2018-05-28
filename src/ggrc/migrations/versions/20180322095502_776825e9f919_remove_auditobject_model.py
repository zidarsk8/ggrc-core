# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Remove AuditObject model

Create Date: 2018-03-22 09:55:02.634448
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import sqlalchemy as sa

from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '776825e9f919'
down_revision = 'b1cb47a3bb3b'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  op.drop_table('audit_objects')


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  op.create_table(
      'audit_objects',
      sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
      sa.Column('modified_by_id', mysql.INTEGER(display_width=11),
                autoincrement=False, nullable=True),
      sa.Column('created_at', mysql.DATETIME(), nullable=False),
      sa.Column('updated_at', mysql.DATETIME(), nullable=False),
      sa.Column('context_id', mysql.INTEGER(display_width=11),
                autoincrement=False, nullable=False),
      sa.Column('audit_id', mysql.INTEGER(display_width=11),
                autoincrement=False, nullable=False),
      sa.Column('auditable_id', mysql.INTEGER(display_width=11),
                autoincrement=False, nullable=False),
      sa.Column('auditable_type', mysql.VARCHAR(length=250), nullable=False),
      sa.ForeignKeyConstraint(['audit_id'], [u'audits.id'],
                              name=u'audit_objects_ibfk_2'),
      sa.ForeignKeyConstraint(['context_id'], [u'contexts.id'],
                              name=u'audit_objects_ibfk_1'),
      sa.PrimaryKeyConstraint('id'),
      mysql_default_charset=u'utf8',
      mysql_engine=u'InnoDB',
  )
