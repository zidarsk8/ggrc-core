# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
update acr table

Create Date: 2018-03-05 20:28:49.737209

"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name


from ggrc.migrations.utils import acr_propagation
from ggrc.migrations.utils import acr_propagation_constants as const

# revision identifiers, used by Alembic.
revision = '3db5f2027c92'
down_revision = '242b8dc8493b'

_AUDIT_FULL_ACCESS = {
    "Relationship R": {
        "Assessment RUD": const.COMMENT_DOCUMENT_RU,
        "AssessmentTemplate RUD": {},
        "Document RU": {},
        "Issue RUD": const.COMMENT_DOCUMENT_RU,
    },
    "Snapshot RU": {},
}

_AUDIT_READ_ACCESS = {
    "Relationship R": {
        "Assessment R": const.COMMENT_DOCUMENT_R,
        "AssessmentTemplate R": {},
        "Document R": {},
        "Issue R": const.COMMENT_DOCUMENT_R,
    },
    "Snapshot R": {},
}

_PROGRAM_OBJECTS_R = (
    "AccessGroup R",
    "Clause R",
    "Contract R",
    # "Control R",  # control is separate due to proposals
    "DataAsset R",
    "Facility R",
    "Issue R",
    "Market R",
    "Objective R",
    "OrgGroup R",
    "Policy R",
    "Process R",
    "Product R",
    "Project R",
    "Regulation R",
    # "Risk R",  # excluded due to proposals
    "RiskAssessment R",
    "Section R",
    "Standard R",
    "System R",
    "Threat R",
    "Vendor R",
)

_PROGRAM_OBJECTS_RUD = (
    "AccessGroup RUD",
    "Clause RUD",
    "Contract RUD",
    # "Control RUD",  # control is separate due to proposals
    "DataAsset RUD",
    "Facility RUD",
    "Issue RUD",
    "Market RUD",
    "Objective RUD",
    "OrgGroup RUD",
    "Policy RUD",
    "Process RUD",
    "Product RUD",
    "Project RUD",
    "Regulation RUD",
    # "Risk RUD",  # excluded due to proposals
    "RiskAssessment RUD",
    "Section RUD",
    "Standard RUD",
    "System RUD",
    "Threat RUD",
    "Vendor RUD",
)

AUTID_PROGRAM_PROPAGATION = {
    "Program": {
        ("Program Managers", "Program Editors"): {
            "Audit RUD": _AUDIT_FULL_ACCESS,
            "Relationship R": {
                "Comment R": {},
                "Document RU": {},
                _PROGRAM_OBJECTS_RUD: const.COMMENT_DOCUMENT_RU,
                ("Control RUD", "Risk RUD"): const.PROPOSAL_RU,
            }
        },
        "Program Readers": {
            "Audit R": _AUDIT_READ_ACCESS,
            "Relationship R": {
                "Comment R": {},
                "Document R": {},
                _PROGRAM_OBJECTS_R: const.COMMENT_DOCUMENT_R,
                ("Control R", "Risk R"): const.PROPOSAL_R,
            }
        },
    },
    "Audit": {
        # Audit captains might also need to get propagated access to program
        # and all program related objects, so that they could clone audits and
        # update all audit snapshots.
        "Audit Captains": _AUDIT_FULL_ACCESS,
        "Auditors": _AUDIT_READ_ACCESS,
    },
}


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  acr_propagation.propagate_roles(AUTID_PROGRAM_PROPAGATION)


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  for object_type, roles_tree in AUTID_PROGRAM_PROPAGATION.items():
    acr_propagation.remove_propagated_roles(object_type, roles_tree.keys())
