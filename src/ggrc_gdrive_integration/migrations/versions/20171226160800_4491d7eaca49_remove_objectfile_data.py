# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Remove ObjectFile data

Create Date: 2017-12-26 16:08:00.683368
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4491d7eaca49'
down_revision = '4bb6fa8fb5e1'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  op.drop_table('object_files')


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  op.create_table(
      'object_files',
      sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
      sa.Column('modified_by_id', mysql.INTEGER(display_width=11),
                autoincrement=False, nullable=True),
      sa.Column('created_at', mysql.DATETIME(), nullable=False),
      sa.Column('updated_at', mysql.DATETIME(), nullable=False),
      sa.Column('context_id', mysql.INTEGER(display_width=11),
                autoincrement=False, nullable=True),
      sa.Column('parent_folder_id', mysql.VARCHAR(length=250), nullable=True),
      sa.Column('file_id', mysql.VARCHAR(length=250), nullable=False),
      sa.Column('fileable_id', mysql.INTEGER(display_width=11),
                autoincrement=False, nullable=False),
      sa.Column('fileable_type', mysql.VARCHAR(length=250), nullable=False),
      sa.PrimaryKeyConstraint('id'),
      mysql_default_charset=u'utf8',
      mysql_engine=u'InnoDB',
  )
  op.create_index('fk_object_files_contexts', 'object_files', ['context_id'])
  op.create_index('ix_object_files_updated_at', 'object_files', ['updated_at'])
