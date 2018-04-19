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
down_revision = '082306b17b07'


_ASSESSMENT_PROPAGATION = {
    ("Creators", "Verifiers"): {
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
            "Document RUD": {},
            "Comment R": {},
            "Issue R": const.COMMENT_DOCUMENT_R,
        },
    },
    "Assignees": {
        "Relationship R": {
            "Snapshot R": {
                "Relationship R": {
                    "Snapshot R": {},
                },
            },
            "Audit R": {
                "Relationship R": {
                    "Document R": {},
                },
            },
            "Document RUD": {},
            "Comment R": {},
            "Issue RUD": const.COMMENT_DOCUMENT_RUD,
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
    _CONTROL_ROLES: const.PROPOSAL_RUD,
}


PROPAGATION = {
    "Assessment": _ASSESSMENT_PROPAGATION,

    "Control": _CONTROL_PROPAGATION,

    "AccessGroup": const.BASIC_PROPAGATION,
    "Clause": const.BASIC_PROPAGATION,
    "Contract": const.BASIC_PROPAGATION,
    "DataAsset": const.BASIC_PROPAGATION,
    "Facility": const.BASIC_PROPAGATION,
    "Issue": const.BASIC_PROPAGATION,
    "Market": const.BASIC_PROPAGATION,
    "Objective": const.BASIC_PROPAGATION,
    "OrgGroup": const.BASIC_PROPAGATION,
    "Policy": const.BASIC_PROPAGATION,
    "Process": const.BASIC_PROPAGATION,
    "Product": const.BASIC_PROPAGATION,
    "Project": const.BASIC_PROPAGATION,
    "Regulation": const.BASIC_PROPAGATION,
    "Section": const.BASIC_PROPAGATION,
    "Standard": const.BASIC_PROPAGATION,
    "System": const.BASIC_PROPAGATION,
    "Threat": const.BASIC_PROPAGATION,
    "Vendor": const.BASIC_PROPAGATION,

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
