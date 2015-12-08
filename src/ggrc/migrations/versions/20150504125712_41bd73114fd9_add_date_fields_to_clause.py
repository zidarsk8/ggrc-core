# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

"""Add date fields to clause

Revision ID: 41bd73114fd9
Revises: 57cc398ad417
Create Date: 2015-05-04 12:57:12.988119

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '41bd73114fd9'
down_revision = '57cc398ad417'


def upgrade():
  op.add_column('sections', sa.Column('end_date', sa.Date(), nullable=True))
  op.add_column('sections', sa.Column('start_date', sa.Date(), nullable=True))


def downgrade():
  op.drop_column('sections', 'start_date')
  op.drop_column('sections', 'end_date')
