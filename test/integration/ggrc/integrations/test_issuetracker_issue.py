# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Integration test for Clonable mixin"""

from mock import patch

from ggrc import db
from ggrc import models
from ggrc.integrations import issues as issues_module
from ggrc.integrations import utils

from integration.ggrc.models import factories
from integration.ggrc.snapshotter import SnapshotterBaseTestCase


class TestIssueTrackerIntegration(SnapshotterBaseTestCase):

  """Test set for IssueTracker integration functionality"""

  # pylint: disable=invalid-name

  def setUp(self):
    # pylint: disable=super-on-old-class
    # pylint seems to get confused, mro chain successfully resolves and returns
    # <type 'object'> as last entry.
    super(TestIssueTrackerIntegration, self).setUp()

    self.client.get("/login")

  # pylint: disable=unused-argument
  @patch('ggrc.integrations.issues.Client.update_issue')
  def test_update_issuetracker_info(self, mock_update_issue):
    """Test that issuetracker issues are updated by the utility"""
    from ggrc.models.hooks import issue_tracker
    with patch.object(issue_tracker, '_is_issue_tracker_enabled',
                      return_value=True):
      iti_issue_id = []
      for _ in range(2):
        iti = factories.IssueTrackerIssueFactory()
        iti_issue_id.append(iti.issue_id)
        asmt = iti.issue_tracked_obj
        asmt_id = asmt.id
        audit = asmt.audit
        self.api.modify_object(audit, {
            "issue_tracker": {
                "enabled": True,
                "component_id": "11111",
                "hotlist_id": "222222",
            },
        })
        asmt = db.session.query(models.Assessment).get(asmt_id)
        self.api.modify_object(asmt, {
            "issue_tracker": {
                "enabled": True,
                "component_id": "11111",
                "hotlist_id": "222222",
            },
        })
        asmt = db.session.query(models.Assessment).get(asmt_id)
        self.api.modify_object(asmt, {
            "issue_tracker": {
                "enabled": True,
                "component_id": "11111",
                "hotlist_id": "222222",
                "issue_priority": "P4",
                "issue_severity": "S3",
            },
        })
      self.api.delete(asmt)
      with patch.object(issues_module.Client, 'update_issue',
                        return_value=None) as mock_method:
        utils.sync_issue_tracker_statuses()
        mock_method.assert_called_once_with(iti_issue_id[0],
                                            {'status': 'ASSIGNED',
                                             'priority': u'P4',
                                             'type': None,
                                             'severity': u'S3'})
