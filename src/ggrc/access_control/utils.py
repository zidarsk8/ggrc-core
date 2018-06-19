# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>


"""Entry point for all acl handlers.

This package should have the single hook that should handle all acl propagation
and deletion.
"""

import logging

import sqlalchemy as sa

from ggrc import db
from ggrc.models import all_models

logger = logging.getLogger(__name__)

# retry count for possible deadlock issues.
PROPAGATION_RETRIES = 10


def insert_select_acls(select_statement):
  """Insert acl records from the select statement
  Args:
    select_statement: sql statement that contains the following columns
      person_id,
      ac_role_id,
      object_id,
      object_type,
      created_at,
      modified_by_id,
      updated_at,
      parent_id,
      parent_id_nn,
  """

  acl_table = all_models.AccessControlList.__table__
  inserter = acl_table.insert().prefix_with("IGNORE")

  last_error = None
  for _ in range(PROPAGATION_RETRIES):
    try:
      last_error = None
      db.session.execute(
          inserter.from_select(
              [
                  acl_table.c.person_id,
                  acl_table.c.ac_role_id,
                  acl_table.c.object_id,
                  acl_table.c.object_type,
                  acl_table.c.created_at,
                  acl_table.c.modified_by_id,
                  acl_table.c.updated_at,
                  acl_table.c.parent_id,
                  acl_table.c.parent_id_nn,
              ],
              select_statement
          )
      )
      db.session.plain_commit()
      break
    except sa.exc.OperationalError as error:
      logger.exception(error)
      last_error = error

  if last_error:
    logger.critical(
        "ACL propagation failed with %d retries on statement: \n %s",
        PROPAGATION_RETRIES,
        select_statement,
    )
    # The following error if exists will only be sa.exc.OperationalError so the
    # pylint warning is invalid.
    raise last_error  # pylint: disable=raising-bad-type
