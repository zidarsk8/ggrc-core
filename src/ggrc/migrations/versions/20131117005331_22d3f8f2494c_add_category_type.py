# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""Add Category#type

Revision ID: 22d3f8f2494c
Revises: 18e1e2aec298
Create Date: 2013-11-17 00:53:31.176635

"""

# revision identifiers, used by Alembic.
revision = '22d3f8f2494c'
down_revision = '18e1e2aec298'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('categories', sa.Column('type', sa.String(length=250), nullable=True))
    op.add_column('categorizations', sa.Column('category_type', sa.String(length=250), nullable=True))


def downgrade():
    op.drop_column('categorizations', 'category_type')
    op.drop_column('categories', 'type')
