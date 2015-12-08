# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""add_notification_object_attributes

Revision ID: 1b9c6ce2ee00
Revises: 40e5d20e1ff
Create Date: 2014-07-22 18:19:31.133320

"""

# revision identifiers, used by Alembic.
revision = '1b9c6ce2ee00'
down_revision = '40e5d20e1ff'

from alembic import op
import sqlalchemy as sa


def upgrade():
  op.add_column('notification_objects', sa.Column('status', sa.String(250), nullable=True))

def downgrade():
  op.drop_column('notification_objects', 'status')
