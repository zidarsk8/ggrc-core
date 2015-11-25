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
down_revision = '35e5344803b4'

from alembic import op
from collections import defaultdict
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


def build_bulk_insert_people_object(reqid, pid):
  return {
      "source_type": "Request",
      "source_id": reqid,
      "destination_type": "Person",
      "destination_id": pid
  }


def build_bulk_insert_rel_attr_object(rel_id, attr_value):
  return {
      "relationship_id": rel_id,
      "attr_name": "AssigneeType",
      "attr_value": ",".join(attr_value)
  }


def get_relationship_id(connection, relationship):
  sid, stype, did, dtype = (relationship["source_id"],
                            relationship["source_type"],
                            relationship["destination_id"],
                            relationship["destination_type"])

  r = connection.execute(relationships_table.select().where(
      and_(
          relationships_table.columns.source_id == sid,
          relationships_table.columns.source_type == stype,
          relationships_table.columns.destination_id == did,
          relationships_table.columns.destination_type == dtype,
      ))).fetchall()
  if r:
    return r[0][0]
  return []


def upgrade():
  connection = op.get_bind()

  # Get all
  requests = connection.execute(requests_table.select()).fetchall()

  # Get all requestors and assigness for each request
  requestor_relationships = [(reqid, rid) for reqid, _, rid in requests if rid]
  assignee_relationships = [(reqid, aid) for reqid, aid, _ in requests if aid]

  # Assign roles separately in case assignee == requester
  request_positions = defaultdict(list)
  for rrid in assignee_relationships:
    request_positions[rrid] += ["Assignee"]

  for rrid in requestor_relationships:
    request_positions[rrid] += ["Requester"]

  # Generate and insert relationship mappings request -> person
  relationships = [build_bulk_insert_people_object(reqid, pid)
                   for reqid, pid in request_positions.keys()]
  op.bulk_insert(relationships_table, relationships)

  # Get relationship IDs, generate assignee types and insert
  # relationship -> relationship_attr
  relationship_attrs = []
  for rel in relationships:
    rel_id = get_relationship_id(connection, rel)
    if rel_id:
      p = request_positions[(rel["source_id"], rel["destination_id"])]
      relationship_attrs += [build_bulk_insert_rel_attr_object(rel_id, p)]
  op.bulk_insert(relationship_attrs_table, relationship_attrs)


def downgrade():
  pass
