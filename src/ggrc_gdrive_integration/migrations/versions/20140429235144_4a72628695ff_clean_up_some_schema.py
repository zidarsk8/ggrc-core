# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""Clean up some schema artifacts

Revision ID: 4a72628695ff
Revises: 420f0f384465
Create Date: 2014-04-29 23:51:44.045058

"""

# revision identifiers, used by Alembic.
revision = '4a72628695ff'
down_revision = '420f0f384465'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


def upgrade():
    op.drop_column('object_events', 'permissions_json')
    op.drop_column('object_files', 'permissions_json')
    op.drop_column('object_folders', 'permissions_json')


def downgrade():
    op.add_column('object_folders', sa.Column('permissions_json', mysql.TEXT(), nullable=False))
    op.add_column('object_files', sa.Column('permissions_json', mysql.TEXT(), nullable=False))
    op.add_column('object_events', sa.Column('permissions_json', mysql.TEXT(), nullable=False))
