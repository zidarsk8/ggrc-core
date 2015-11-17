# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

"""Make person email not null

Revision ID: 1bad7fe16295
Revises: 29b63100d61c
Create Date: 2015-11-07 12:30:18.465786

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1bad7fe16295'
down_revision = '29b63100d61c'


def upgrade():
  op.execute("DELETE FROM people WHERE email IS NULL")
  op.alter_column("people", "email", nullable=False,
                  existing_type=sa.String(length=250))


def downgrade():
  op.alter_column("people", "email", nullable=True,
                  existing_type=sa.String(length=250))
