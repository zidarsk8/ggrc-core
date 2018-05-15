# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Add parent id nn to acl table

Create Date: 2018-04-30 00:58:40.172905
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'e5f737f2a428'
down_revision = '2795c6d50e62'


def _remove_acl_duplicates():
  """Remove duplicate entries in acl entry.

  Because our unique index on ACL table contains a nullable column, we can have
  duplicates of the top most items that have parent_id set to null.

  Because we want to avoid that we'll change the unique constraint to a non
  nullable field and for that we must first remove any duplicate entry that
  would cause the migration to fail.
  """
  acl_table = sa.sql.table(
      "access_control_list",
      sa.sql.column('id', sa.Integer),
  )
  connection = op.get_bind()
  duplicates_query = connection.execute("""
      select
        group_concat(id),
        count(id) as count
      from access_control_list
      where
        parent_id is null
      group by
        `person_id`,
        `ac_role_id`,
        `object_id`,
        `object_type`
      having count > 1
  """)

  duplicates = []
  for ids_string, _ in duplicates_query.fetchall():
    ids = ids_string.split(",")
    duplicates.extend(ids[1:])

  op.execute(
      acl_table.delete().where(
          acl_table.c.id.in_(duplicates)
      )
  )


def _add_parent_id_nn_column():
  """Add parent_id_nn column and make it non nullable.

  The creation of the column and making it non nullable are done in separate
  steps to avoid mysql warnings for missing values.
  """
  op.add_column(
      'access_control_list',
      sa.Column(
          'parent_id_nn',
          sa.Integer(),
          server_default="0",
          nullable=True,
      ),
  )

  op.execute("update access_control_list set parent_id_nn = parent_id")
  op.execute("""
      update access_control_list
      set parent_id_nn = 0
      where parent_id_nn is null
  """)

  op.alter_column(
      'access_control_list',
      'parent_id_nn',
      existing_type=sa.Integer(),
      server_default="0",
      nullable=False,
  )


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""

  _remove_acl_duplicates()
  _add_parent_id_nn_column()

  op.create_index(
      'idx_object_type_object_id_parent_id_nn',
      'access_control_list',
      ['object_type', 'object_id', 'parent_id_nn'],
      unique=False,
  )

  op.create_unique_constraint(
      'uq_access_control_list',
      'access_control_list',
      ['person_id', 'ac_role_id', 'object_id', 'object_type', 'parent_id_nn'],
  )
  op.drop_index('person_id', table_name='access_control_list')


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  op.create_unique_constraint(
      'person_id',
      'access_control_list',
      ['person_id', 'ac_role_id', 'object_id', 'object_type', 'parent_id'],
  )
  op.drop_index('uq_access_control_list', table_name='access_control_list')
  op.drop_index(
      'idx_object_type_object_id_parent_id_nn',
      table_name='access_control_list'
  )
  op.drop_column('access_control_list', 'parent_id_nn')
