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
down_revision = 'b46bdb31d869'


COMMENTABLE_SCOPING_TABLES = {
    "AccessGroup": "access_groups",
    "DataAsset": "data_assets",
    "Facility": "facilities",
    "Market": "markets",
    "Metric": "metrics",
    "OrgGroup": "org_groups",
    # "Process", is included in systems table
    "Product": "product_groups",
    "ProductGroup": "products",
    "Project": "projects",
    "System": "systems",
    "TechnologyEnvironment": "technology_environments",
    "Vendor": "vendors",
}


revision_queue = sa.sql.table(
    'objects_without_revisions',
    sa.Column('obj_id', sa.Integer),
    sa.Column('obj_type', sa.String(length=250)),
    sa.Column('action', sa.String(length=250)),
)


def _select_ids(table_name, object_type):
  object_table = sa.sql.table(
      table_name,
      sa.Column('id', sa.Integer),
      sa.Column('recipients', sa.String(length=250)),
  )

  return sa.select([
      object_table.c.id,
      sa.literal(object_type).label("obj_type"),
      sa.literal("modified").label("action"),
  ]).select_from(
      object_table
  )


def _select_system_ids(object_type, table_name):
  object_table = sa.sql.table(
      table_name,
      sa.Column('id', sa.Integer),
      sa.Column('is_biz_process', sa.String(length=250)),
      sa.Column('recipients', sa.String(length=250)),
  )

  return sa.select([
      object_table.c.id,
      sa.literal(object_type).label("obj_type"),
      sa.literal("modified").label("action"),
  ]).select_from(
      object_table
  ).where(
      object_table.c.is_biz_process == (object_type == "Process")
  )

def _insert_revision_queue(object_type, table_name):
  if object_type in ["System", "Process"]:
    ids_select = _select_system_ids(object_type, table_name)
  else:
    ids_select = _select_ids(table_name, object_type)

  inserter = revision_queue.insert().prefix_with("IGNORE")
  op.execute(inserter.from_select(
      [
          revision_queue.c.obj_id,
          revision_queue.c.obj_type,
          revision_queue.c.action,
      ],
      ids_select
  ))


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  for object_type, table_name in COMMENTABLE_SCOPING_TABLES.items():
    commentable_table = sa.sql.table(
        table_name,
        sa.Column('id', sa.Integer),
        sa.Column('recipients', sa.String(length=250)),
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

    _insert_revision_queue(object_type, table_name)



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
