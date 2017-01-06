# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Migrate audits for snapshots

Create Date: 2016-11-17 11:49:04.547216
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

from logging import getLogger

from alembic import op

from sqlalchemy.sql import and_
from sqlalchemy.sql import column
from sqlalchemy.sql import func
from sqlalchemy.sql import select
from sqlalchemy.sql import table
from sqlalchemy.sql import tuple_

from ggrc.models.event import Event
from ggrc.models.relationship import Relationship
from ggrc.models.revision import Revision
from ggrc.models.snapshot import Snapshot
from ggrc.models.assessment import Assessment
from ggrc.models.issue import Issue

from ggrc.migrations.utils import get_relationship_cache
from ggrc.migrations.utils import get_revisions
from ggrc.migrations.utils import insert_payloads
from ggrc.migrations.utils import Stub

from ggrc.migrations.utils.migrator import get_migration_user_id

from ggrc.snapshotter.rules import Types


logger = getLogger(__name__)  # pylint: disable=invalid-name


# revision identifiers, used by Alembic.
revision = '142272c4a0b6'
down_revision = '579239d161e1'

relationships_table = Relationship.__table__
events_table = Event.__table__
snapshots_table = Snapshot.__table__
revisions_table = Revision.__table__

assessments_table = Assessment.__table__
issues_table = Issue.__table__

audits_table = table(
    "audits",
    column("id"),
    column("context_id"),
    column("program_id"),
)

programs_table = table(
    "programs",
    column("id"),
    column("context_id")
)


def create_snapshots(connection, user_id, caches, audits):
  """Create snapshots and relationships to programs"""
  # pylint: disable=too-many-locals
  relationships_payload = []
  snapshots_payload = []
  snapshot_quads = set()

  program_relationships = caches["program_rels"]
  audit_relationships = caches["audit_rels"]
  program_contexts = caches["program_contexts"]
  revisions_cache = caches["revisions"]

  for audit in audits:
    parent_key = Stub("Audit", audit.id)
    program_key = Stub("Program", audit.program_id)
    audit_scope_objects = audit_relationships[parent_key]
    program_scope_objects = program_relationships[program_key]
    missing_in_program_scope = audit_scope_objects - program_scope_objects

    if missing_in_program_scope:
      for obj_ in missing_in_program_scope:
        if obj_ in revisions_cache:
          relationships_payload += [{
              "source_type": "Program",
              "source_id": audit.program_id,
              "destination_type": obj_.type,
              "destination_id": obj_.id,
              "modified_by_id": user_id,
              "context_id": program_contexts[audit.program_id],
          }]

    if audit_scope_objects:
      for obj_ in audit_scope_objects:
        if obj_ in revisions_cache:
          quad = ("Audit", audit.id, obj_.type, obj_.id)
          snapshot_quads.add(quad)
          snapshots_payload += [{
              "parent_type": "Audit",
              "parent_id": audit.id,
              "child_type": obj_.type,
              "child_id": obj_.id,
              "revision_id": revisions_cache[obj_],
              "context_id": audit.context_id,
              "modified_by_id": user_id,
          }]
          # this is because of our hack where we rely on relationships
          # to actually show objects
          relationships_payload += [{
              "source_type": "Audit",
              "source_id": audit.id,
              "destination_type": obj_.type,
              "destination_id": obj_.id,
              "modified_by_id": user_id,
              "context_id": audit.context_id,
          }]
        else:
          logger.warning(
              "Missing revision for object %s-%s", obj_.type, obj_.id)

  insert_payloads(connection, snapshots_payload, relationships_payload)
  return snapshot_quads


def process_audits(connection, user_id, caches, audits):
  """Process audits"""
  snapshot_quads = create_snapshots(connection, user_id, caches, audits)

  relationships_payload = []
  if snapshot_quads:
    snapshots = connection.execute(select([snapshots_table]).where(
        tuple_(
            Snapshot.parent_type,
            Snapshot.parent_id,
            Snapshot.child_type,
            Snapshot.child_id,
        ).in_(snapshot_quads)
    )).fetchall()
    snapshot_cache = {
        (obj_.parent_type, obj_.parent_id,
         obj_.child_type, obj_.child_id): (obj_.id, obj_.context_id)
        for obj_ in snapshots
    }
    for snapshot in snapshot_quads:
      relationships_payload += [{
          "source_type": snapshot[2],
          "source_id": snapshot[3],
          "destination_type": "Snapshot",
          "destination_id": snapshot_cache[snapshot][0],
          "modified_by_id": user_id,
          "context_id": snapshot_cache[snapshot][1],
      }]

    if relationships_payload:
      connection.execute(
          relationships_table.insert().prefix_with("IGNORE"),
          relationships_payload)


def validate_database(connection):
  """Validate that there are no invalid objects in the database before performing
  any operations"""
  # pylint: disable=too-many-locals
  audits_more = []
  ghost_objects = []

  tables = [
      ("Assessment", assessments_table),
      ("Issue", issues_table),
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

    result_zero = all_object_ids - to_audit_mapped_ids

    if result_more:
      audits_more += [(klass_name, result_more)]
    if result_zero:
      ghost_objects += [(klass_name, result_zero)]
  return audits_more, ghost_objects


def upgrade():
  """Migrate audit-related data and concepts to audit snapshots"""
  # pylint: disable=too-many-locals

  connection = op.get_bind()

  audits_more, ghost_objects = validate_database(connection)

  if audits_more or ghost_objects:
    if audits_more:
      for klass_name, result in audits_more:
        ids = [id_ for _, id_ in result]
        logger.warning(
            "The following %s have more than one Audit: %s",
            klass_name,
            ",".join(map(str, ids))  # pylint: disable=bad-builtin
        )
    if ghost_objects:
      for klass_name, result in ghost_objects:
        logger.warning(
            "The following %s have no Audits mapped to them: %s",
            klass_name,
            ",".join(map(str, result))  # pylint: disable=bad-builtin
        )
    raise Exception("Cannot perform migration. Check logger warnings.")

  audits = connection.execute(audits_table.select()).fetchall()
  if audits:
    program_ids = {audit.program_id for audit in audits}

    program_sql = select([programs_table]).where(
        programs_table.c.id.in_(program_ids)
    )
    programs = connection.execute(program_sql)
    program_contexts = {program.id: program.context_id for program in programs}

    program_relationships = get_relationship_cache(
        connection, "Program", Types.all)
    audit_relationships = get_relationship_cache(
        connection, "Audit", Types.all)

    all_objects = (program_relationships.values() +
                   audit_relationships.values())
    revisionable_objects = set()
    revisionable_objects = revisionable_objects.union(*all_objects)
    revision_cache = get_revisions(connection, revisionable_objects)

    objects_missing_revision = (revisionable_objects -
                                set(revision_cache.keys()))
    if objects_missing_revision:
      missing = ",".join(
          ["{obj.type}-{obj.id}".format(obj=obj)
           for obj in objects_missing_revision])
      logger.warning(
          "The following objects are missing revisions: %s", missing)
      raise Exception("There are still objects with missing revisions!")

    caches = {
        "program_contexts": program_contexts,
        "program_rels": program_relationships,
        "audit_rels": audit_relationships,
        "revisions": revision_cache
    }

    user_id = get_migration_user_id(connection)

    process_audits(connection, user_id, caches, audits)


def downgrade():
  pass
