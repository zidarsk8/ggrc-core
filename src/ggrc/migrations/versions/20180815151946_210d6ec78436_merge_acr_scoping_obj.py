# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Add new ACR Assignee, Verifier, Compliance Contacts and merge Contacts

Create Date: 2018-08-15 15:19:46.890174
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

from alembic import op
import sqlalchemy as sa

from ggrc.migrations import utils
from ggrc.migrations.utils.migrator import get_migration_user_id
from ggrc.migrations.utils import \
    acr_propagation_constants_scoping_objects_merge_roles \
    as scoping_objects_rules
from ggrc.migrations.utils import acr_propagation

# revision identifiers, used by Alembic.
revision = '210d6ec78436'
down_revision = '31cde07a1abe'


SCOPING_OBJECTS = [
    "AccessGroup",
    "DataAsset",
    "Facility",
    "Market",
    "Metric",
    "OrgGroup",
    "Process",
    "Product",
    "ProductGroup",
    "Project",
    "System",
    "TechnologyEnvironment",
    "Vendor",
]

NEW_ROLES = [
    "Assignee",
    "Verifier",
    "Compliance Contacts",
]

MANDATORY = {
    "Assignee": 1,
    "Verifier": 1,
    "Compliance Contacts": 0,
}

DEFAULT_TO_CURRENT_USER = {
    "Assignee": 1,
    "Verifier": 1,
    "Compliance Contacts": 0,
}

DESTINATION_ROLE = "Compliance Contacts"

SOURCE_ROLES = ["Primary Contacts", "Secondary Contacts"]


def _add_roles_for_objects(objects, new_roles):
  """
    Creates new roles in acr for a given list of objects.
  :param objects: object names for which new roles should be added
  :param new_roles: list of roles to add into the acr
  """
  connection = op.get_bind()
  user_id = get_migration_user_id(connection)

  update_entries = []
  for object_name in objects:
    for role_name in new_roles:
      update_entries.append(
          "('{}', '{}', NOW(), NOW(), {}, 1, {}, {})".format(
              role_name,
              object_name,
              user_id,
              MANDATORY[role_name],
              DEFAULT_TO_CURRENT_USER[role_name]
          )
      )
  insert_sql = """
      INSERT INTO access_control_roles (
          name,
          object_type,
          created_at,
          updated_at,
          modified_by_id,
          non_editable,
          mandatory,
          default_to_current_user
      ) values """ + ", ".join(update_entries)
  connection.execute(insert_sql)


def _merge_role_acl(object_types, source_role, destination_role):
  """Merge one role ACL to another."""
  ROLE_IDS_MAPPING = {}
  connection = op.get_bind()
  for object_type in object_types:
    destination_role_query = connection.execute(sa.text("""
        SELECT id
        FROM access_control_roles
        WHERE object_type = :object_type and name = :name
    """), {"object_type": object_type, "name": destination_role})
    destination_role_id = [result for result in destination_role_query][0][0]

    source_role_query = connection.execute(sa.text("""
        SELECT id
        FROM access_control_roles
        WHERE object_type = :object_type and name = :name
    """), {"object_type": object_type, "name": source_role})
    source_role_id = [result for result in source_role_query][0][0]

    ROLE_IDS_MAPPING[source_role_id] = destination_role_id

  # Collect objects with changings ACL for create_missing_revisions
  for _id in ROLE_IDS_MAPPING.keys():
    response = connection.execute(
        sa.text("""
        SELECT object_id, object_type
        FROM access_control_list
        WHERE ac_role_id = (:role)
        """),
        role=str(_id)
    )
    for row in response:
      utils.add_to_objects_without_revisions(
          connection, row.object_id, row.object_type, "modified"
      )

  # Move ACL from source role to destignation role
  for source_role_id, destination_role_id in ROLE_IDS_MAPPING.items():
    connection.execute(
        sa.text(
            """
            UPDATE IGNORE access_control_list
            SET ac_role_id = :destination_role_id
            WHERE ac_role_id = :source_role_id
            """
        ),
        {"source_role_id": source_role_id,
         "destination_role_id": destination_role_id}
    )

  # Collect new ACLs for create_missing_revisions
  for _id in ROLE_IDS_MAPPING.values():
      response = connection.execute(
          sa.text("""
          SELECT id
          FROM access_control_list
          WHERE ac_role_id = (:role)
          """),
          role=str(_id)
      )
      for row in response:
        utils.add_to_objects_without_revisions(
            connection, row.id, "AccessControlList", "created"
        )


def _delete_roles_for_objects(objects, roles_to_delete):
  """
    Removes roles for a given list of objects.
  :param objects: object names for which new roles should be removed
  :param roles_to_delete: list of roles to delete from the acr
  """
  connection = op.get_bind()
  for object_name in objects:
    for role_to_delete in roles_to_delete:
      connection.execute(
          sa.text("""DELETE FROM access_control_roles
                  WHERE name = :name and object_type = :object_type"""),
          {"name": role_to_delete, "object_type": object_name}
      )


def create_acl_record(connection, person_id, ac_role_id,
                      object_id, object_type):
  """Creates ACL record"""
  connection.execute("""
      INSERT INTO access_control_list
      (person_id, ac_role_id, object_id, object_type, created_at,
      modified_by_id, updated_at,  context_id, parent_id, parent_id_nn)
      VALUES
      ({}, {}, {}, "{}", NOW(), NULL, NOW(), NULL, NULL, 0);
      """.format(person_id, ac_role_id, object_id, object_type))
  # utils.add_to_objects_without_revisions(
  #             connection, acl.id, "AccessControlList", "created"
  #         )


def _populate_mandatory_roles(objects):
  """Assign one admin of object as Assignee/Verifier if them not assigned"""
  TABLES = {
      "AccessGroup": "access_groups",
      "DataAsset": "data_assets",
      "Facility": "facilities",
      "Market": "markets",
      "Metric": "metrics",
      "OrgGroup": "org_groups",
      "Product": "product_groups",
      "ProductGroup": "products",
      "Project": "projects",
      "System": "systems",
      "Process": "systems",  # TODO IS IT OK?
      "TechnologyEnvironment": "technology_environments",
      "Vendor": "vendors",
  }
  query = """
      SELECT
          obj.id AS obj_id,
          "{obj_type}" AS object_type,
          acl_a.person_id AS 'assignee',
          acl_v.person_id AS 'verifier',
          acl_adm.person_id AS 'admin'
      FROM {table} AS obj
      LEFT JOIN
      (   SELECT acl1.object_id, acl1.person_id
          FROM access_control_roles AS acr1
          JOIN access_control_list AS acl1
          ON acl1.ac_role_id = acr1.id
          WHERE acr1.name = "Assignee"
              AND acl1.object_type = "{obj_type}") AS acl_a
      ON acl_a.object_id = obj.id
      LEFT JOIN
      (   SELECT acl1.object_id, acl1.person_id
          FROM access_control_roles AS acr1
          JOIN access_control_list AS acl1
          ON acl1.ac_role_id = acr1.id
          WHERE acr1.name = "Verifier"
              AND acl1.object_type = "{obj_type}") AS acl_v
      ON acl_v.object_id = obj.id
      LEFT JOIN
      (   SELECT acl1.object_id, acl1.person_id
          FROM access_control_roles AS acr1
          JOIN access_control_list AS acl1
          ON acl1.ac_role_id = acr1.id
          WHERE acr1.name = "Admin"
              AND acl1.object_type = "{obj_type}"
          LIMIT 1) AS acl_adm
      ON acl_adm.object_id = obj.id
  """
  connection = op.get_bind()
  for object_name in objects:
    response = connection.execute(
        query.format(table=TABLES[object_name], obj_type=object_name)
    )
    assignee_role_id = connection.execute("""
        SELECT id FROM access_control_roles
        WHERE object_type = "{}" AND name = "Assignee"
    """.format(object_name)).fetchone()[0]
    verifier_role_id = connection.execute("""
        SELECT id FROM access_control_roles
        WHERE object_type = "{}" AND name = "Verifier"
    """.format(object_name)).fetchone()[0]
    for row in response:
      if row.assignee is None:
        create_acl_record(connection, row.admin, assignee_role_id,
                          row.obj_id, row.object_type)
      if row.verifier is None:
        create_acl_record(connection, row.admin, verifier_role_id,
                          row.obj_id, row.object_type)


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  # Add Assignee, Verifier roles
  _add_roles_for_objects(SCOPING_OBJECTS, NEW_ROLES)
  # Propagate Assignee, Verifier roles
  acr_propagation.propagate_roles(
      scoping_objects_rules.GGRC_NEW_ROLES_PROPAGATION,
      with_update=True
  )

  # Move Primary Contacts to Compliance Contacts
  for src_role in SOURCE_ROLES:
    _merge_role_acl(SCOPING_OBJECTS, src_role, DESTINATION_ROLE)

  # Remove Secondary Contacts role from acr tree
  for object_type, roles_tree in \
          scoping_objects_rules.GGRC_TO_DELETE_ROLES_PROPAGATION.items():
    acr_propagation.remove_propagated_roles(object_type, roles_tree.keys())

  # Populate Assignee/Verifier with Admin
  _populate_mandatory_roles(SCOPING_OBJECTS)


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""

  # Propagate Secondary Contact role
  acr_propagation.propagate_roles(
      scoping_objects_rules.GGRC_TO_DELETE_ROLES_PROPAGATION,
      with_update=True
  )

  # Remove Assignee, Verifier roles from acr tree
  for object_type, roles_tree in \
          scoping_objects_rules.GGRC_NEW_ROLES_PROPAGATION.items():
    acr_propagation.remove_propagated_roles(object_type, roles_tree.keys())

  # Delete Assignee, Verifier roles
  _delete_roles_for_objects(SCOPING_OBJECTS, NEW_ROLES)
