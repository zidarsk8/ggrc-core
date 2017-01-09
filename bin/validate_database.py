# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Validate audit relationships in a db.

To manually specify a db just export GGRC_DATABASE_URI
Example:
  GGRC_DATABASE_URI="mysql+mysqldb://root:root@localhost/ggrcdev?charset=utf8"
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.

# pylint: disable=invalid-name

import sys
import csv
from collections import defaultdict

from sqlalchemy.sql import and_
from sqlalchemy.sql import func
from sqlalchemy.sql import select

# We have to import app before we can use db and other parts of the app.
from ggrc import app  # noqa  pylint: disable=unused-import
from ggrc import db
from ggrc.models import all_models

from ggrc.models.relationship import Relationship
from ggrc.models.assessment import Assessment
from ggrc.models.issue import Issue


def validate_database():
  """Check if the database is in a valid state for Audit migrations.

  The Audit snapshot migration does not produce correct results if any
  Assessment or Issue are not mapped to exactly one Audit. This function
  checks and outputs the ids of the offending objects and returns a non zero
  code if any such object is found.
  """

  # pylint: disable=too-many-locals
  multiple_mappings = []
  zero_mappings = []
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

    result_left_more = db.session.execute(sql_left_more).fetchall()
    result_right_more = db.session.execute(sql_right_more).fetchall()
    result_more = result_left_more + result_right_more

    result_left_one = db.session.execute(sql_left_one).fetchall()
    result_right_one = db.session.execute(sql_right_one).fetchall()
    result_one = result_left_one + result_right_one

    all_object_ids = {
        x.id for x in db.session.execute(select([table_.c.id])).fetchall()
    }
    to_audit_mapped_ids = {
        x.object_id for x in result_more + result_one
    }

    result_zero = all_object_ids - to_audit_mapped_ids

    if result_more:
      multiple_mappings += [(klass_name, result_more)]
    if result_zero:
      zero_mappings += [(klass_name, result_zero)]
  return multiple_mappings, zero_mappings


def _generate_delete_csv(all_bad_ids):
  """Generate a CSV file for deleting bad objects."""
  data = []
  for model_name, ids in all_bad_ids.items():
    model = getattr(all_models, model_name, None)
    if not model:
      print "Incorrect model found:", model_name
      sys.exit(1)

    slugs = db.session.query(model.slug).filter(model.id.in_(ids))
    data += [
        ["Object type", "", ""],
        [model.__name__, "Code", "Delete"],
    ]
    for row in slugs:
      data.append(["", row.slug, "force"])
    data.append(["", "", ""])

  with open("/vagrant/delete_invalid_data.csv", "wb") as csv_file:
    writer = csv.writer(csv_file)
    for row in data:
      writer.writerow(row)


def validate():
  """Migrate audit-related data and concepts to audit snapshots"""
  print "Checking database: {}".format(db.engine)

  tables = set(row[0] for row in db.session.execute("show tables"))

  if {"relationships", "issues", "assessments"}.difference(tables):
    # Ignore checks if required tables do not exist. This is if the check is
    # run on an empty database (usually with db_reset)
    return

  multiple_mappings, zero_mappings = validate_database()

  all_bad_ids = defaultdict(list)
  if multiple_mappings or zero_mappings:
    for klass_name, result in multiple_mappings:
      ids = [id_ for _, id_ in result]
      all_bad_ids[klass_name] += ids
      print "Too many Audits mapped to {klass}: {ids}".format(
          klass=klass_name,
          ids=",".join(str(id_) for id_ in sorted(ids))
      )
    for klass_name, ids in zero_mappings:
      all_bad_ids[klass_name] += ids
      print "No Audits mapped to {klass}: {ids}".format(
          klass=klass_name,
          ids=",".join(str(id_) for id_ in sorted(ids))
      )
    _generate_delete_csv(all_bad_ids)
    print "To remove all violating objects import delete_invalid_data.csv."
    print "FAIL"
    sys.exit(1)
  else:
    print "PASS"
    sys.exit(0)


if __name__ == "__main__":
  validate()
