# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Remove parent_id column

Create Date: 2018-07-07 07:13:58.203708
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from alembic import op


# revision identifiers, used by Alembic.
revision = '054d15be7a29'
down_revision = '84e537a5aede'


def upgrade():
  """Upgrade database data, creating a new revision."""

  op.drop_column('categories', 'parent_id')
  op.drop_constraint(
      'clauses_ibfk_3',
      table_name='clauses',
      type_='foreignkey',
  )
  op.drop_column('clauses', 'parent_id')
  op.drop_constraint(
      'controls_ibfk_2',
      table_name='controls',
      type_='foreignkey',
  )
  op.drop_column('controls', 'parent_id')
  op.drop_constraint(
      'sections_ibfk_2',
      table_name='sections',
      type_='foreignkey',
  )
  op.drop_column('sections', 'parent_id')


def downgrade():
  """Downgrade database data back to the previous revision."""

  op.add_column('sections', sa.Column('parent_id',
                                      mysql.INTEGER(display_width=11),
                                      autoincrement=False,
                                      nullable=True))
  op.create_foreign_key(
      u'sections_ibfk_2',
      'sections',
      'sections',
      ['parent_id'],
      ['id'],
  )
  op.add_column('controls', sa.Column('parent_id',
                                      mysql.INTEGER(display_width=11),
                                      autoincrement=False,
                                      nullable=True))
  op.create_foreign_key(
      u'controls_ibfk_2',
      'controls',
      'controls',
      ['parent_id'],
      ['id']
  )
  op.add_column('clauses', sa.Column('parent_id',
                                     mysql.INTEGER(display_width=11),
                                     autoincrement=False,
                                     nullable=True))
  op.create_foreign_key(
      u'clauses_ibfk_3',
      'clauses',
      'clauses',
      ['parent_id'],
      ['id']
  )
  op.add_column('categories', sa.Column('parent_id',
                                        mysql.INTEGER(display_width=11),
                                        autoincrement=False,
                                        nullable=True))
