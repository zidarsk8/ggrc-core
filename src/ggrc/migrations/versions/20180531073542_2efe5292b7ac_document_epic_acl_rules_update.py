# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Document epic ACL rules update

Create Date: 2018-05-31 07:35:42.717362
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name
from alembic import op
from ggrc.migrations.utils import acr_propagation_constants_evidence_comments \
    as prev_rules
from ggrc.migrations.utils import acr_propagation_document_epic \
    as doc_epic_rules
from ggrc.migrations.utils import acr_propagation


# revision identifiers, used by Alembic.
revision = '2efe5292b7ac'
down_revision = 'f77f9a8aff84'


def disallow_to_delete_doc():
  """Update Document admin to remove delete permissions"""
  sql = """
      UPDATE access_control_roles acr SET acr.delete=0
      WHERE acr.name="Admin" AND acr.object_type="Document"
  """
  op.execute(sql)


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  old_rules = prev_rules.GGRC_PROPAGATION
  new_rules = doc_epic_rules.GGRC_PROPAGATION
  acr_propagation.update_acr_propagation_tree(old_rules, new_rules)
  disallow_to_delete_doc()


def allow_to_delete_doc():
  """Update Document admin to add delete permissions"""
  sql = """
      UPDATE access_control_roles acr SET acr.delete=1
      WHERE acr.name="Admin" AND acr.object_type="Document"
  """
  op.execute(sql)


def downgrade():
  """Downgrade database schema and/or data back to the previous revision.

  To downgrade you need first to downgrade
  1) alembic ggrc_risks downgrade -1
  2) alembic ggrc_basic_permissions downgrade -1
  """
  allow_to_delete_doc()
  old_rules = doc_epic_rules.GGRC_PROPAGATION
  new_rules = prev_rules.GGRC_PROPAGATION
  acr_propagation.update_acr_propagation_tree(old_rules, new_rules)
