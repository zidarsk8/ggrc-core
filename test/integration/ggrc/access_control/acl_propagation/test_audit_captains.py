# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test Access Control roles Audit Captains propagation."""

import ddt

from ggrc.models import all_models
from integration.ggrc.access_control import rbac_factories
from integration.ggrc.access_control.acl_propagation import base
from integration.ggrc.utils import helpers


@ddt.ddt
class TestAuditorsPropagation(base.TestACLPropagation):
  """Test Audit Captains role permissions propagation."""

  PERMISSIONS = {
      "Creator": {
          "Audit": {
              "read": True,
              "update": True,
              "delete": True,
              "clone": (True, "unimplemented"),
              "read_revisions": True,
              "map_control": True,
              "map_external_control": (False, "unimplemented"),
              "deprecate": True,
              "archive": False,
              "unarchive": (False, "unimplemented"),
              "summary": True,
          },
          "Assessment": {
              "create": True,
              "generate": True,
              "read": True,
              "update": True,
              "delete": True,
              "read_revisions": True,
              "map_snapshot": True,
              "deprecate": True,
              "map_comment": True,
              "map_evidence": True,
              "related_assessments": True,
              "related_objects": True,
              "complete": True,
              "in_progress": True,
              "not_started": True,
              "decline": (False, "unimplemented"),
              "verify": (False, "unimplemented"),
          },
          "AssessmentTemplate": {
              "create": True,
              "read": True,
              "update": True,
              "delete": True,
              "read_revisions": True,
          },
          "Snapshot Assessment": {
              "read": True,
              "read_original": False,
              "update": True,
              "get_latest_version": (True, "unimplemented"),
          },
          "Snapshot Audit": {
              "read": True,
              "read_original": False,
              "update": True,
              "get_latest_version": (True, "unimplemented"),
          },
          "Issue Assessment": {
              "read": True,
              "update": True,
              "delete": True,
              "read_revisions": True,
              "map": False,
              "create_and_map": True,
              "raise_issue": True,
              "unmap": True,
          },
          "Issue Audit": {
              "read": True,
              "update": True,
              "delete": True,
              "read_revisions": True,
              "map": False,
              "create_and_map": True,
              "unmap": True,
          },
          "Evidence Audit": {
              "create_and_map": True,
              "read": True,
              "update": True,
              "delete": False,
              "read_comments": True,
              "add_comment": True
          },
          "Evidence Assessment": {
              "create_and_map": True,
              "read": True,
              "update": True,
              "delete": False,
              "read_comments": True,
              "add_comment": True
          }
      },
      "Reader": {
          "Audit": {
              "read": True,
              "update": True,
              "delete": True,
              "clone": (True, "unimplemented"),
              "read_revisions": True,
              "map_control": True,
              "map_external_control": (False, "unimplemented"),
              "deprecate": True,
              "archive": False,
              "unarchive": (False, "unimplemented"),
              "summary": True,
          },
          "Assessment": {
              "create": True,
              "generate": True,
              "read": True,
              "update": True,
              "delete": True,
              "read_revisions": True,
              "map_snapshot": True,
              "deprecate": True,
              "map_comment": True,
              "map_evidence": True,
              "related_assessments": True,
              "related_objects": True,
              "complete": True,
              "in_progress": True,
              "not_started": True,
              "decline": (False, "unimplemented"),
              "verify": (False, "unimplemented"),
          },
          "AssessmentTemplate": {
              "create": True,
              "read": True,
              "update": True,
              "delete": True,
              "read_revisions": True,
          },
          "Snapshot Assessment": {
              "read": True,
              "read_original": True,
              "update": True,
              "get_latest_version": True,
          },
          "Snapshot Audit": {
              "read": True,
              "read_original": True,
              "update": True,
              "get_latest_version": True,
          },
          "Issue Assessment": {
              "read": True,
              "update": True,
              "delete": True,
              "read_revisions": True,
              "map": False,
              "create_and_map": True,
              "raise_issue": True,
              "unmap": True,
          },
          "Issue Audit": {
              "read": True,
              "update": True,
              "delete": True,
              "read_revisions": True,
              "map": False,
              "create_and_map": True,
              "unmap": True,
          },
          "Evidence Audit": {
              "create_and_map": True,
              "read": True,
              "update": True,
              "delete": False,
              "read_comments": True,
              "add_comment": True
          },
          "Evidence Assessment": {
              "create_and_map": True,
              "read": True,
              "update": True,
              "delete": False,
              "read_comments": True,
              "add_comment": True
          }

      },
      "Editor": {
          "Audit": {
              "read": True,
              "update": True,
              "delete": True,
              "clone": True,
              "read_revisions": True,
              "map_control": True,
              "map_external_control": True,
              "deprecate": True,
              "archive": False,
              "unarchive": (False, "unimplemented"),
              "summary": True,
          },
          "Assessment": {
              "create": (False, "unimplemented"),
              "generate": (False, "unimplemented"),
              "read": True,
              "update": True,
              "delete": True,
              "read_revisions": True,
              "map_snapshot": True,
              "deprecate": True,
              "map_comment": True,
              "map_evidence": True,
              "related_assessments": True,
              "related_objects": True,
              "complete": True,
              "in_progress": True,
              "not_started": True,
              "decline": (False, "unimplemented"),
              "verify": (False, "unimplemented"),
          },
          "AssessmentTemplate": {
              "create": True,
              "read": True,
              "update": True,
              "delete": True,
              "read_revisions": True,
          },
          "Snapshot Assessment": {
              "read": True,
              "read_original": True,
              "update": True,
              "get_latest_version": True,
          },
          "Snapshot Audit": {
              "read": True,
              "read_original": True,
              "update": True,
              "get_latest_version": True,
          },
          "Issue Assessment": {
              "read": True,
              "update": True,
              "delete": True,
              "read_revisions": True,
              "map": True,
              "create_and_map": True,
              "raise_issue": True,
              "unmap": True,
          },
          "Issue Audit": {
              "read": True,
              "update": True,
              "delete": True,
              "read_revisions": True,
              "map": True,
              "create_and_map": True,
              "unmap": True,
          },
          "Evidence Audit": {
              "create_and_map": True,
              "read": True,
              "update": True,
              "delete": False,
              "read_comments": True,
              "add_comment": True
          },
          "Evidence Assessment": {
              "create_and_map": True,
              "read": True,
              "update": True,
              "delete": False,
              "read_comments": True,
              "add_comment": True
          }
      },
  }

  def init_factory(self, role, model, parent):
    """Initialize RBAC factory with propagated Audit Captains role.

    Args:
        role: Global Custom role that user have (Creator/Reader/Editor).
        model: Model name for which factory should be got.
        parent: Model name in scope of which objects should be installed.

    Returns:
        Initialized RBACFactory object.
    """
    self.setup_people()
    captain_acr = all_models.AccessControlRole.query.filter_by(
        name="Audit Captains",
        object_type="Audit",
    ).first()

    rbac_factory = rbac_factories.TEST_FACTORIES_MAPPING[model]
    return rbac_factory(self.people[role].id, captain_acr, parent)

  @helpers.unwrap(PERMISSIONS)
  def test_access(self, role, model, action_name, expected_result):
    self.runtest(role, model, action_name, expected_result)
