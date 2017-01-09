# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Database validation for Audit snapshots migration."""

from sqlalchemy.sql import and_
from sqlalchemy.sql import func
from sqlalchemy.sql import select

from ggrc.models.relationship import Relationship
from ggrc.models.assessment import Assessment
from ggrc.models.issue import Issue


def validate_database(connection):
  """Check if the database is in a valid state for Audit migrations.

  The Audit snapshot migration does not produce correct results if any
  Assessment or Issue are not mapped to exactly one Audit. This function
  checks and outputs the ids of the offending objects and returns a non zero
  code if any such object is found.
  """

  # pylint: disable=too-many-locals
  multiple_mappings = {}
  zero_mappings = {}

  relationships_table = Relationship.__table__
  assessments_table = Assessment.__table__
  issues_table = Issue.__table__

  tables = [
      ("Assessment", assessments_table),
      ("Issue", issues_table),
      # "Request",  ignoring requests since they have an audit foreign key and
      # can not be in an invalid state.
  ]

  for (klass_name, table_) in tables:
    sql_base_left = select([
        func.count(relationships_table.c.id).label("relcount"),
        relationships_table.c.source_id.label("object_id"),
    ]).where(
        and_(
            relationships_table.c.source_type == klass_name,
            relationships_table.c.destination_type == "Audit"
        )
    ).group_by(relationships_table.c.source_id)

    sql_base_right = select([
        func.count(relationships_table.c.id).label("relcount"),
        relationships_table.c.destination_id.label("object_id"),
    ]).where(
        and_(
            relationships_table.c.destination_type == klass_name,
            relationships_table.c.source_type == "Audit"
        )
    ).group_by(relationships_table.c.destination_id)

    sql_left_more = sql_base_left.having(sql_base_left.c.relcount > 1)
    sql_right_more = sql_base_right.having(sql_base_right.c.relcount > 1)
    sql_left_one = sql_base_left.having(sql_base_left.c.relcount == 1)
    sql_right_one = sql_base_right.having(sql_base_right.c.relcount == 1)

    result_left_more = connection.execute(sql_left_more).fetchall()
    result_right_more = connection.execute(sql_right_more).fetchall()
    result_more = result_left_more + result_right_more

    result_left_one = connection.execute(sql_left_one).fetchall()
    result_right_one = connection.execute(sql_right_one).fetchall()
    result_one = result_left_one + result_right_one

    all_object_ids = {
        x.id for x in connection.execute(select([table_.c.id])).fetchall()
    }
    to_audit_mapped_ids = {
        x.object_id for x in result_more + result_one
    }

    zero_mapped_ids = all_object_ids - to_audit_mapped_ids
    multiple_mapped_ids = [id_ for _, id_ in result_more]

    if multiple_mapped_ids:
      multiple_mappings[klass_name] = multiple_mapped_ids
    if zero_mapped_ids:
      zero_mappings[klass_name] = zero_mapped_ids
  return multiple_mappings, zero_mappings
