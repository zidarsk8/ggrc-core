# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: andraz@reciprocitylabs.com
# Maintained By: andraz@reciprocitylabs.com

"""drop commentable from comments

Revision ID: 29b63100d61c
Revises: 4cd52e0a17b8
Create Date: 2015-10-29 10:48:59.510325

"""

# revision identifiers, used by Alembic.
revision = '29b63100d61c'
down_revision = '4cd52e0a17b8'

from alembic import op
import sqlalchemy as sa


def upgrade():
  op.drop_column('comments', 'commentable_id')
  op.drop_column('comments', 'commentable_type')


def downgrade():
  op.add_column('comments',
      sa.Column('commentable_id', sa.Integer(), nullable=False)
  )
  op.add_column('comments',
      sa.Column('commentable_type', sa.String(length=250), nullable=False)
  )
