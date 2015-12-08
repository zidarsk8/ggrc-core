# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""Nullable request objective

Revision ID: 3fa5cf4f8ae6
Revises: 58da8a74882c
Create Date: 2013-12-12 01:18:06.300862

"""

# revision identifiers, used by Alembic.
revision = '3fa5cf4f8ae6'
down_revision = '58da8a74882c'

from alembic import op
import sqlalchemy as sa


def upgrade():
  op.alter_column('requests', 'objective_id',
      existing_type = sa.Integer(),
      nullable = True
    )


def downgrade():
  op.execute('SET FOREIGN_KEY_CHECKS = 0')

  op.alter_column('requests', 'objective_id',
      existing_type = sa.Integer(),
      nullable = False
    )

  op.execute('SET FOREIGN_KEY_CHECKS = 1')
