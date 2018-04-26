# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
update acr table

Create Date: 2018-03-05 20:28:49.737209
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import sqlalchemy as sa

from alembic import op

from ggrc.migrations.utils import acr_propagation
from ggrc.migrations.utils import acr_propagation_constants as const


# revision identifiers, used by Alembic.
revision = '3db5f2027c92'
down_revision = 'fcd5e64ff664'


def _add_parent_id_column():
  """Add parent id column to access control roles table."""
  op.add_column('access_control_roles', sa.Column(
      'parent_id', sa.Integer(), nullable=True))
  op.create_foreign_key(
      "fk_access_control_roles_parent_id",
      "access_control_roles", "access_control_roles",
      ["parent_id"], ["id"],
      ondelete="CASCADE"
  )


def _remove_parent_id_column():
  """Remove parent id column from access control roles table."""
  op.drop_constraint(
      "fk_access_control_roles_parent_id",
      "access_control_roles",
      "foreignkey",
  )
  op.drop_column('access_control_roles', 'parent_id')


def _add_assessment_roles_tree():
  acr_propagation.propagate_roles(const.GGRC_PROPAGATION)


def _copy_current_acl_table():
  """Create semi temporary backup tables for old ACLs.

  These backups should only exist for one release in case we would need to
  downgrade the release to previous version.
  """
  op.execute("DROP TABLE IF EXISTS acl_copy")
  op.execute("""
      CREATE TABLE `acl_copy` (
          `id` int(11) NOT NULL DEFAULT '0',
          `person_id` int(11) NOT NULL,
          `ac_role_id` int(11) NOT NULL,
          `object_id` int(11) NOT NULL,
          `object_type` varchar(250) NOT NULL,
          `created_at` datetime NOT NULL,
          `modified_by_id` int(11) DEFAULT NULL,
          `updated_at` datetime NOT NULL,
          `context_id` int(11) DEFAULT NULL,
          `parent_id` int(11) DEFAULT NULL
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8
  """)
  op.execute("DROP TABLE IF EXISTS acr_copy")
  op.execute("""
      CREATE TABLE `acr_copy` (
          `id` int(11) NOT NULL DEFAULT '0',
          `name` varchar(250) NOT NULL,
          `object_type` varchar(250) DEFAULT NULL,
          `tooltip` varchar(250) DEFAULT NULL,
          `read` tinyint(1) NOT NULL DEFAULT '1',
          `update` tinyint(1) NOT NULL DEFAULT '1',
          `delete` tinyint(1) NOT NULL DEFAULT '1',
          `my_work` tinyint(1) NOT NULL DEFAULT '1',
          `created_at` datetime NOT NULL,
          `modified_by_id` int(11) DEFAULT NULL,
          `updated_at` datetime NOT NULL,
          `context_id` int(11) DEFAULT NULL,
          `mandatory` tinyint(1) NOT NULL DEFAULT '0',
          `default_to_current_user` tinyint(1) NOT NULL DEFAULT '0',
          `non_editable` tinyint(1) NOT NULL DEFAULT '0',
          `internal` tinyint(1) NOT NULL DEFAULT '0',
          `notify_about_proposal` tinyint(1) NOT NULL DEFAULT '0'
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8
  """)
  op.execute("INSERT INTO acr_copy SELECT * FROM access_control_roles")
  op.execute("INSERT INTO acl_copy SELECT * FROM access_control_list")


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  _copy_current_acl_table()
  _add_parent_id_column()
  _add_assessment_roles_tree()
  acr_propagation.remove_deprecated_roles([
      "Assignees Document Mapped",
      "Assignees Mapped",
      "Creators Document Mapped",
      "Creators Mapped",
      "Verifiers Document Mapped",
      "Verifiers Mapped",
  ])


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""

  connection = op.get_bind()
  ids = connection.execute("""
      select
        acl.id,
        acl.object_type,
        acl.object_id,
        p.email,
        acr.name
      from acl_copy as acl
      left join people as p on
        acl.person_id = p.id
      left join access_control_roles as acr on
        acl.ac_role_id = acr.id
      where
        acl.parent_id is null and
        acl.id not in (select id from access_control_list)
  """).fetchall()
  print "ACL entries that will be reintroduced by this downgrade:"
  for row in ids:
    print row

  ids = connection.execute("""
      select
        acl.id,
        acl.object_type,
        acl.object_id,
        p.email,
        acr.name
      from access_control_list as acl
      left join people as p on
        acl.person_id = p.id
      left join access_control_roles as acr on
        acl.ac_role_id = acr.id
      where
        acl.parent_id is null and
        acl.id not in (select id from acl_copy)
  """).fetchall()
  print "ACL entries that will not be propagated properly by this downgrade:"
  print "To fix these roles please manually remove and re-add them."
  for row in ids:
    print row

  for object_type, roles_tree in const.GGRC_PROPAGATION.items():
    acr_propagation.remove_propagated_roles(object_type, roles_tree.keys())
  _remove_parent_id_column()

  op.execute("INSERT IGNORE INTO access_control_roles SELECT * from acr_copy")
  op.execute("INSERT IGNORE INTO access_control_list SELECT * from acl_copy")
