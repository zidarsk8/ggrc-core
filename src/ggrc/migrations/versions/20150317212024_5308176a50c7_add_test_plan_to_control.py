# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""Add test_plan to Control

Revision ID: 5308176a50c7
Revises: 1f7d8208aff2
Create Date: 2015-03-02 21:20:24.014188

"""

# revision identifiers, used by Alembic.
revision = '5308176a50c7'
down_revision = '1f7d8208aff2'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
  op.add_column('controls', sa.Column('test_plan', sa.Text(), nullable=True))

def downgrade():
  op.drop_column('controls', 'test_plan')
