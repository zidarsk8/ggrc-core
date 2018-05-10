# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
create audit relationships

Create Date: 2018-03-19 19:07:05.594851
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = '082306b17b07'
down_revision = '7c9d15c78b0f'


def _cleanup_relationships(meta):
  """Remove audit relationships for direct mappings."""
  relationships = meta.tables["relationships"]
  op.execute(
      relationships.delete().where(
          sa.and_(
              relationships.c.source_type == "Audit",
              relationships.c.destination_type == "Program",
          )
      )
  )
  op.execute(
      relationships.delete().where(
          sa.and_(
              relationships.c.destination_type == "Audit",
              relationships.c.source_type == "Program",
          )
      )
  )
  op.execute(
      relationships.delete().where(
          sa.and_(
              relationships.c.source_type == "Audit",
              relationships.c.destination_type == "Snapshot",
          )
      )
  )
  op.execute(
      relationships.delete().where(
          sa.and_(
              relationships.c.destination_type == "Audit",
              relationships.c.source_type == "Snapshot",
          )
      )
  )


def _insert_relationships(meta, select_statement):
  """Insert selected rows into relationships table."""
  relationships = meta.tables["relationships"]

  op.execute(
      relationships.insert().from_select(
          [
              relationships.c.modified_by_id,
              relationships.c.created_at,
              relationships.c.updated_at,
              relationships.c.source_type,
              relationships.c.source_id,
              relationships.c.destination_type,
              relationships.c.destination_id,
              relationships.c.is_external,
          ],
          select_statement
      )
  )


def _create_program_relationships(meta):
  """Create relationships between programs and audits."""
  audits = meta.tables["audits"]

  select_statement = sa.select([
      audits.c.modified_by_id,
      sa.func.now(),
      sa.func.now(),
      sa.literal("Program"),
      audits.c.program_id,
      sa.literal("Audit"),
      audits.c.id,
      sa.literal("0"),
  ]).select_from(audits)

  _insert_relationships(meta, select_statement)


def _create_snapshot_relationships(meta):
  """Create relationships between programs and audits."""
  snapshots = meta.tables["snapshots"]

  select_statement = sa.select([
      snapshots.c.modified_by_id,
      sa.func.now(),
      sa.func.now(),
      sa.literal("Audit"),
      snapshots.c.parent_id,
      sa.literal("Snapshot"),
      snapshots.c.id,
      sa.literal("0"),
  ]).select_from(snapshots)

  _insert_relationships(meta, select_statement)


def get_meta():
  """Get schema metadata."""
  bind = op.get_bind()
  meta = sa.MetaData()
  meta.reflect(bind=bind)
  return meta


def upgrade():
  """Create missing audit relationships.

  There are some obsolete relationships in the database already, so this
  function first does the cleanup and then creates new ones. Since the
  relationships that already exist are invalid by our code before this
  migration, we can have the same cleanup in the downgrade without losing any
  of our data.
  """
  meta = get_meta()

  _cleanup_relationships(meta)
  _create_program_relationships(meta)
  _create_snapshot_relationships(meta)


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  meta = get_meta()

  _cleanup_relationships(meta)
