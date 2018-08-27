# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Update recipients fields

Create Date: 2018-08-15 15:00:26.228846
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import sqlalchemy as sa
from sqlalchemy import func

from alembic import op

# revision identifiers, used by Alembic.
revision = '31cde07a1abe'
down_revision = 'fe3ce1807a4e'


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

    # replace all None data with empty string for recipients field
    op.execute(commentable_table.update()
               .where(commentable_table.c.recipients.is_(None))
               .values(recipients=''))

    # remove Primary Contacts from recipients list
    op.execute(commentable_table.update().values(
        recipients=func.replace(commentable_table.c.recipients,
                                "Primary Contacts,", "")))
    op.execute(commentable_table.update().values(
        recipients=func.replace(commentable_table.c.recipients,
                                "Primary Contacts", "")))

    # remove Secondary Contacts from recipients list
    op.execute(commentable_table.update().values(
        recipients=func.replace(commentable_table.c.recipients,
                                "Secondary Contacts,", "")))
    op.execute(commentable_table.update().values(
        recipients=func.replace(commentable_table.c.recipients,
                                "Secondary Contacts", "")))

    # add Assignee, Verifier, Compliance Contacts to recipients list
    op.execute(commentable_table.update()
               .where(commentable_table.c.recipients != '')
               .values(recipients=func.concat(commentable_table.c.recipients,
                                              ",Assignee,Verifier,"
                                              "Compliance Contacts")))
    op.execute(commentable_table.update()
               .where(commentable_table.c.recipients == '')
               .values(recipients=func.concat(commentable_table.c.recipients,
                                              "Assignee,Verifier,"
                                              "Compliance Contacts")))


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  for name in COMMENTABLE_SCOPING_TABLES:
    commentable_table = sa.sql.table(
        name, sa.Column('recipients', sa.String(length=250))
    )
    # remove new roles and
    # put to all recipients list Primary Contacts and Secondary Contacts
    op.execute(commentable_table.update().values(
        recipients=func.replace(commentable_table.c.recipients,
                                "Assignee,Verifier,Compliance Contacts",
                                "Primary Contacts,Secondary Contacts")))

    # trim commas from all recipients lists
    connection = op.get_bind()
    connection.execute(
        sa.text("UPDATE {} SET recipients=TRIM(',' FROM recipients)"
                .format(commentable_table.name)))
