# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: urban@reciprocitylabs.com
# Maintained By: urban@reciprocitylabs.com

"""Migrate data to request FCO

Revision ID: 3c1619ff36e8
Revises: 27684e5f313a
Create Date: 2015-11-10 13:46:05.350000

"""

# revision identifiers, used by Alembic.
revision = '3c1619ff36e8'
down_revision = '27684e5f313a'

from alembic import op
from sqlalchemy.sql import table, column
from sqlalchemy.sql.expression import and_

requests_table = table(
    'requests',
    column('id'),
    column('assignee_id'),
    column('requestor_id'))

relationships_table = table(
    'relationships',
    column('id'),
    column('source_id'),
    column('source_type'),
    column('destination_id'),
    column('destination_type'),
)

relationship_attrs_table = table(
    'relationship_attrs',
    column('relationship_id'),
    column('attr_name'),
    column('attr_value'),
)


def build_bulk_insert_object(reqid, pid):
  return {
      "source_type": "Request",
      "source_id": reqid,
      "destination_type": "Person",
      "destination_id": pid
  }


def insert_relationship_attributes(connection,
                                   relationships,
                                   attr_type,
                                   attr_value):
  relationship_attrs = []
  for rel in relationships:
    rel = connection.execute(relationships_table.select().where(
        and_(
            relationships_table.columns.source_id == rel["source_id"],
            relationships_table.columns.source_type == rel["source_type"],
            relationships_table.columns.destination_id ==
            rel["destination_id"],
            relationships_table.columns.destination_type ==
            rel["destination_type"],
        ))).fetchall()
    if rel:
      relid, _, _, _, _ = rel[0]
      relationship_attrs += [{
          "relationship_id": relid,
          "attr_name": attr_type,
          "attr_value": attr_value
      }]
  op.bulk_insert(relationship_attrs_table, relationship_attrs)


def upgrade():
  connection = op.get_bind()

  req_relationships = connection.execute(requests_table.select()).fetchall()

  requestor_relationships = [
      build_bulk_insert_object(reqid, rid)
      for reqid, aid, rid in req_relationships if rid and rid != aid]
  assignee_relationships = [
      build_bulk_insert_object(reqid, aid)
      for reqid, aid, rid in req_relationships if aid]

  op.bulk_insert(relationships_table, requestor_relationships)
  op.bulk_insert(relationships_table, assignee_relationships)

  insert_relationship_attributes(connection, requestor_relationships,
                                 "AssigneeType", "Requester")
  insert_relationship_attributes(connection, assignee_relationships,
                                 "AssigneeType", "Assignee")


def downgrade():
  pass
