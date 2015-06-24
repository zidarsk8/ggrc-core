# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

"""Drop is_enabled column

Revision ID: 1d1e9807c46c
Revises: 3261848aaa2b
Create Date: 2015-06-11 12:42:44.520839

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1d1e9807c46c'
down_revision = '3261848aaa2b'


def upgrade():
  op.drop_column('people', 'is_enabled')


def downgrade():
  op.add_column(
      'people',
      sa.Column('is_enabled',
                mysql.TINYINT(display_width=1),
                autoincrement=False, nullable=False))
