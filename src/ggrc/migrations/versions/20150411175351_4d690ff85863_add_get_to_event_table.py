# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

"""add get to event table

Revision ID: 4d690ff85863
Revises: 5180ce718082
Create Date: 2015-04-11 17:53:51.630881

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4d690ff85863'
down_revision = '5180ce718082'


def upgrade():
  op.alter_column(
      'events', 'action',
      type_=sa.Enum(u'POST', u'PUT', u'DELETE', u'IMPORT', u'GET'),
      existing_type=sa.Enum(u'POST', u'PUT', u'DELETE', u'IMPORT'),
      nullable=False
  )


def downgrade():
  op.alter_column(
      'events', 'action',
      type_=sa.Enum(u'POST', u'PUT', u'DELETE', u'IMPORT'),
      existing_type=sa.Enum(
          u'POST', u'PUT', u'DELETE', u'IMPORT', u'GET'),
      nullable=False
  )
