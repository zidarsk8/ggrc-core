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
from ggrc.migrations.utils import acr_propagation_constants


# revision identifiers, used by Alembic.
revision = '3db5f2027c92'
down_revision = '082306b17b07'

_ASSESSMENT_ROLES = ("Creators", "Assignees", "Verifiers")

_ASSESSMENT_PROPAGATION = {
    _ASSESSMENT_ROLES: {
        "Relationship R": {
            "Audit R": {
                "Relationship R": {
                    "Document R": {},
                },
            },
            "Snapshot R": {
                "Relationship R": {
                    "Snapshot R": {},
                },
            },
            "Document RU": {},
            "Comment R": {},
            "Issue R": acr_propagation_constants.COMMENT_DOCUMENT_R,
        },
    },
}

_CONTROL_ROLES = (
    "Admin",
    "Primary Contacts",
    "Secondary Contacts",
    "Principal Assignees",
    "Secondary Assignees",
)

_CONTROL_PROPAGATION = {
    _CONTROL_ROLES: acr_propagation_constants.PROPOSAL_RU,
}


PROPAGATION = {
    "Assessment": _ASSESSMENT_PROPAGATION,

    "Control": _CONTROL_PROPAGATION,

    "AccessGroup": acr_propagation_constants.BASIC_PROPAGATION,
    "Clause": acr_propagation_constants.BASIC_PROPAGATION,
    "Contract": acr_propagation_constants.BASIC_PROPAGATION,
    "DataAsset": acr_propagation_constants.BASIC_PROPAGATION,
    "Facility": acr_propagation_constants.BASIC_PROPAGATION,
    "Issue": acr_propagation_constants.BASIC_PROPAGATION,
    "Market": acr_propagation_constants.BASIC_PROPAGATION,
    "Objective": acr_propagation_constants.BASIC_PROPAGATION,
    "OrgGroup": acr_propagation_constants.BASIC_PROPAGATION,
    "Policy": acr_propagation_constants.BASIC_PROPAGATION,
    "Process": acr_propagation_constants.BASIC_PROPAGATION,
    "Product": acr_propagation_constants.BASIC_PROPAGATION,
    "Project": acr_propagation_constants.BASIC_PROPAGATION,
    "Regulation": acr_propagation_constants.BASIC_PROPAGATION,
    "Section": acr_propagation_constants.BASIC_PROPAGATION,
    "Standard": acr_propagation_constants.BASIC_PROPAGATION,
    "System": acr_propagation_constants.BASIC_PROPAGATION,
    "Threat": acr_propagation_constants.BASIC_PROPAGATION,
    "Vendor": acr_propagation_constants.BASIC_PROPAGATION,

    # "RiskAssessment": does not have ACL roles
}


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
  acr_propagation.propagate_roles(PROPAGATION)


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  _add_parent_id_column()
  _add_assessment_roles_tree()


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  for object_type, roles_tree in PROPAGATION.items():
    acr_propagation.remove_propagated_roles(object_type, roles_tree.keys())
  _remove_parent_id_column()
