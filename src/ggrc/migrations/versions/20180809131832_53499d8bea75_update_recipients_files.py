# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Update recipients files

Create Date: 2018-08-09 13:18:32.732660
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '53499d8bea75'
down_revision = 'd617da1998ef'


COMMENTABLE_SCOPING_TABLES = [
    "access_groups",
    "data_assets",
    "facilities",
    "markets",
    "metrics",
    "org_groups",
    "systems",
    "products",
    "product_groups",
    "projects",
    "technology_environments",
    "vendors"
]


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  for name in COMMENTABLE_SCOPING_TABLES:
    commentable_table = sa.sql.table(
        name, sa.Column('recipients', sa.String(length=250))
    )
    op.execute(commentable_table.update().values(
        recipients="Admin,Primary Contacts,Secondary Contacts,"
                   "Product Managers,Technical Leads,"
                   "Technical / Program Managers,"
                   "Legal Counsels,System Owners"
    ))


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  for name in COMMENTABLE_SCOPING_TABLES:
    commentable_table = sa.sql.table(
        name, sa.Column('recipients', sa.String(length=250))
    )
    op.execute(commentable_table.update().values(
        recipients="Admin,Primary Contacts,Secondary Contacts"
    ))
