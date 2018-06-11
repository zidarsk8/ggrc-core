# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Add evidence comment RBAC rule

Create Date: 2018-05-13 12:55:25.402295
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

from ggrc.migrations.utils import acr_propagation_constants_document_epic \
    as prev_rules
from ggrc.migrations.utils import acr_propagation_constants_evidence_comments \
    as doc_epic_evid_comments
from ggrc.migrations.utils import acr_propagation


# revision identifiers, used by Alembic.
revision = 'e6127a4956b1'
down_revision = 'c76730859bd3'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  old_rules = prev_rules.GGRC_PROPAGATION
  new_rules = doc_epic_evid_comments.GGRC_PROPAGATION
  acr_propagation.update_acr_propagation_tree(old_rules, new_rules)


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  old_rules = doc_epic_evid_comments.GGRC_PROPAGATION
  new_rules = prev_rules.GGRC_PROPAGATION
  acr_propagation.update_acr_propagation_tree(old_rules, new_rules)
