# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: andraz@reciprocitylabs.com
# Maintained By: andraz@reciprocitylabs.com

"""Add Comments

Revision ID: 4cd52e0a17b8
Revises: 3c8f204ba7a9
Create Date: 2015-10-23 13:00:18.555497

"""

# revision identifiers, used by Alembic.
revision = '4cd52e0a17b8'
down_revision = '27684e5f313a'

from alembic import op
import sqlalchemy as sa


def upgrade():
  op.create_table(
      'comments',
      sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
      sa.Column('description', sa.Text()),
      sa.Column('created_at', sa.DateTime()),
      sa.Column('modified_by_id', sa.Integer()),
      sa.Column('updated_at', sa.DateTime()),
      sa.Column('context_id', sa.Integer(), sa.ForeignKey('contexts.id'))
  )


def downgrade():
  op.drop_table('comments')
