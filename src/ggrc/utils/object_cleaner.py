# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Utility for cleaning up orphan db entries on polymorphic joins

mysql> select table_name, column_name, data_type
from information_schema.columns
where table_schema="ggrcdev" and column_name like '%_type%';
+-------------------------------+-----------------------+-----------+
| table_name                    | column_name           | data_type | Ignored
+-------------------------------+-----------------------+-----------+
| access_control_list           | object_type           | varchar   |
| access_control_roles          | object_type           | varchar   | -
| assessment_templates          | template_object_type  | varchar   | -
| assessments                   | assessment_type       | varchar   | -
| attribute_definitions         | attribute_type_id     | int       | -
| attribute_types               | attribute_type_id     | int       | -
| attribute_types               | field_type            | varchar   | -
| attributes                    | object_type           | varchar   |
| attributes                    | source_type           | varchar   | -
| audit_objects                 | auditable_type        | varchar   |
| audits                        | object_type           | varchar   | -
| automappings                  | source_type           | varchar   | -
| automappings                  | destination_type      | varchar   | -
| categorizations               | categorizable_type    | varchar   |
| categorizations               | category_type         | varchar   | -
| comments                      | assignee_type         | text      | -
| contexts                      | related_object_type   | varchar   |
| custom_attribute_definitions  | definition_type       | varchar   |
| custom_attribute_definitions  | attribute_type        | varchar   |
| custom_attribute_values       | attributable_type     | varchar   | -
| cycle_task_group_object_tasks | task_type             | varchar   | -
| documents                     | document_type         | enum      | -
| events                        | resource_type         | varchar   | -
| notification_configs          | notif_type            | varchar   | -
| notifications                 | object_type           | varchar   |
| notifications                 | notification_type_id  | int       | -
| object_documents              | documentable_type     | varchar   |
| object_events                 | eventable_type        | varchar   |
| object_files                  | fileable_type         | varchar   |
| object_folders                | folderable_type       | varchar   |
| object_owners                 | ownable_type          | varchar   |
| object_people                 | personable_type       | varchar   |
| object_templates              | object_type_id        | int       | -
| object_types                  | object_type_id        | int       |
| object_types                  | parent_object_type_id | int       |
| relationships                 | source_type           | varchar   |
| relationships                 | destination_type      | varchar   |
| revisions                     | resource_type         | varchar   | -
| revisions                     | source_type           | varchar   | -
| revisions                     | destination_type      | varchar   | -
| risk_objects                  | object_type           | varchar   |
| snapshots                     | parent_type           | varchar   |
| snapshots                     | child_type            | varchar   |
| task_group_objects            | object_type           | varchar   | -
| task_group_tasks              | task_type             | varchar   | -
+-------------------------------+-----------------------+-----------+
45 rows in set (0.00 sec)

Notes for the polymorphic links that are ignored by this module.

- attributes
    source_id
    source_type
    - these are ignored because those attributes should have been recalculated
      and not just removed. If there is an orphan object here, then we have
      bigger issues.

- task_group_objects
    We used to allow original to be deleted and it would show up on a task as
    deleted. Not sure if that is still the case, but this should not affect
    object counts overall.

- custom_attribute_values
    attribute_value
    attribute_object_id
    - attribute_value and attribute_object_id are also polymorphic but ignored
      since we can only map people like that and we do not support deleting
      people from our app.

- custom_attribute_definitions
    definition_id
    definition_type
    - These are special as they allow id to be null


Tables and attributes that are handled by this module:

- access_control_list
- attributes
- audit_objects
- categorizations
- contexts
- custom_attribute_values
- notifications
- object_documents
- object_events
- object_files
- object_folders
- object_owners
- object_people
- relationships
- relationships
- risk_objects
"""

import logging

from ggrc import db
from ggrc.models import all_models


logger = logging.getLogger(__name__)

CLEANUP_TABLES = [
    ("access_control_list", "object_id", "object_type"),
    ("audit_objects", "auditable_id", "auditable_type"),
    ("categorizations", "categorizable_id", "categorizable_type"),
    ("contexts", "related_object_id", "related_object_type"),
    ("custom_attribute_values", "attributable_id", "attributable_type"),
    ("notifications", "object_id", "object_type"),
    ("object_documents", "documentable_id", "documentable_type"),
    ("object_events", "eventable_id", "eventable_type"),
    ("object_files", "fileable_id", "fileable_type"),
    ("object_folders", "folderable_id", "folderable_type"),
    ("object_owners", "ownable_id", "ownable_type"),
    ("object_people", "personable_id", "personable_type"),
    ("relationships", "source_id", "source_type"),
    ("relationships", "destination_id", "destination_type"),
    ("risk_objects", "object_id", "object_type"),
]


SPECIAL_TABLES = [
    ("custom_attribute_definitions", "definition_id", "definition_type"),
    ("attributes", "object_id", "object_type"),
]


def _clean_orphan_entries(table_name, column_id, column_type, dry_run=True):
  """Remove all invalid database entries for deleted objects.

  This function should remove all database entries with polymorphic link to a
  deleted object.

  For safety reasons we will only delete entries that address a deleted object
  of an existing model. Entries for deleted models (such as Requests) are not
  handled by this function.

  Args:
    table_name: Table with polymorphic join.
    column_id: Name of the column with id field.
    column_type: Name of the column with type field.
  """
  logger.info("Cleaning orphan objects for %s with (%s, %s)",
              table_name, column_id, column_type)

  for model in all_models.all_models:
    removed = db.session.execute(
        """
        select
            '{table_name}',
            id,
            {column_type},
            {column_id}
        from {table_name}
        where
            {column_type} = :model_type and
            {column_id} not in (
                select id from {model_table_name}
            )
        """.format(
            table_name=table_name,
            column_type=column_type,
            column_id=column_id,
            model_table_name=model.__tablename__,
        ),
        {"model_type": model.__name__},
    ).fetchall()
    if removed and not dry_run:
      removed_string = [unicode(row) for row in removed]
      if len(removed_string) > 20:
        removed_string = removed_string[:10] + ["..."] + removed_string[-10:]
      logger.critical(
          "Removing %s orphan objects:\n%s",
          len(removed),
          "\n".join(removed_string),
      )
      db.session.execute(
          """
          delete
          from {table_name}
          where
              {column_type} = :model_type and
              {column_id} not in (
                  select id from {model_table_name}
              )
          """.format(
              table_name=table_name,
              column_type=column_type,
              column_id=column_id,
              model_table_name=model.__tablename__,
          ),
          {"model_type": model.__name__},
      )
      db.session.commit()


def clean_all_orphan_entries():
  for table_name, column_id, column_type in CLEANUP_TABLES:
    _clean_orphan_entries(table_name, column_id, column_type, dry_run=False)
