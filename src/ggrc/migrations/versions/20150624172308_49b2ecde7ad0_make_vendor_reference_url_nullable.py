# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

"""Make vendor reference_url nullable

Revision ID: 49b2ecde7ad0
Revises: 1306a9036135
Create Date: 2015-06-24 17:23:08.955375

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49b2ecde7ad0'
down_revision = '1306a9036135'


def upgrade():
  op.alter_column("vendors", "reference_url", nullable=True,
                  existing_type=sa.String(length=250))


def downgrade():
  op.alter_column("vendors", "reference_url", nullable=False,
                  existing_type=sa.String(length=250))
