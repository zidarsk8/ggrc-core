# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Integration tests for Issue with IssueTracker integration."""

import mock
import ddt

from ggrc import models
from ggrc import settings
from ggrc.models import all_models

from integration.ggrc.models import factories
from integration import ggrc
from integration.ggrc.api_helper import Api


@ddt.ddt
class TestIssueIntegration(ggrc.TestCase):
  """Test set for IssueTracker integration functionality."""

  # pylint: disable=invalid-name

  def setUp(self):
    # pylint: disable=super-on-old-class
    super(TestIssueIntegration, self).setUp()
    self.api = Api()
    self.client.get("/login")

  @mock.patch("ggrc.integrations.issues.Client.create_issue",
              return_value={"issueId": "issueId"})
  def test_create_issue_tracker_info(self, mock_create_issue):
    """Test creation issue tracker issue for Issue object."""
    component_id = "1234"
    hotlist_id = "4321"
    issue_type = "Default Issue type"
    issue_priority = "Default Issue priority"
    issue_severity = "Default Issue severity"
    random_title = factories.random_str()

    with mock.patch.object(settings, "ISSUE_TRACKER_ENABLED", True):
      response = self.api.post(all_models.Issue, {
          "issue": {
              "title": random_title,
              "context": None,
              "issue_tracker": {
                  "enabled": True,
                  "component_id": component_id,
                  "hotlist_id": hotlist_id,
                  "issue_type": issue_type,
                  "issue_priority": issue_priority,
                  "issue_severity": issue_severity,
              }
          },
      })
      mock_create_issue.assert_called_once()
      self.assertEqual(response.status_code, 201)
      issue_id = response.json.get("issue").get("id")
      issue_tracker_issue = models.IssuetrackerIssue.get_issue("Issue",
                                                               issue_id)
      self.assertTrue(issue_tracker_issue.enabled)
      self.assertEqual(issue_tracker_issue.title, random_title)
      self.assertEqual(issue_tracker_issue.component_id, component_id)
      self.assertEqual(issue_tracker_issue.hotlist_id, hotlist_id)
      self.assertEqual(issue_tracker_issue.issue_type, issue_type)
      self.assertEqual(issue_tracker_issue.issue_priority, issue_priority)
      self.assertEqual(issue_tracker_issue.issue_severity, issue_severity)

  @ddt.data(
      ({"description": "new description"},
       {"comment": "Issue Description has been updated.\nnew description"}),
      ({"test_plan": "new test plan"},
       {"comment": "Issue Remediation Plan has been updated.\nnew test plan"}),
      ({"issue_tracker": {"component_id": "123", "enabled": True}},
       {"component_id": u"123"}),
      ({"issue_tracker": {"hotlist_id": "321", "enabled": True}},
       {"hotlist_id": u"321"}),
      ({"issue_tracker": {"issue_priority": "new priority", "enabled": True}},
       {"priority": "new priority"}),
      ({"issue_tracker": {"issue_severity": "new severity", "enabled": True}},
       {"severity": "new severity"}),
      ({"issue_tracker": {"enabled": False}},
       {"comment": "Changes to this GGRC object will no "
                   "longer be tracked within this bug."}),
  )
  @ddt.unpack
  @mock.patch("ggrc.integrations.issues.Client.update_issue")
  def test_update_issue(self, issue_attrs, expected_query, mock_update_issue):
    """Test updating issue tracker issue."""
    iti = factories.IssueTrackerIssueFactory(
        enabled=True,
        issue_tracked_obj=factories.IssueFactory()
    )
    with mock.patch.object(settings, "ISSUE_TRACKER_ENABLED", True):
       self.api.put(iti.issue_tracked_obj, issue_attrs)
    mock_update_issue.assert_called_with(iti.issue_id, expected_query)

  @mock.patch("ggrc.integrations.issues.Client.update_issue")
  def test_delete_issue(self, mock_update_issue):
    """Test updating issue tracker issue when issue in GGRC has been deleted"""
    iti = factories.IssueTrackerIssueFactory(
        enabled=True,
        issue_tracked_obj=factories.IssueFactory()
    )
    expected_query = {"status": "OBSOLETE",
                      "comment": "Changes to this GGRC object will no longer "
                                 "be tracked within this bug."}
    with mock.patch.object(settings, "ISSUE_TRACKER_ENABLED", True):
      self.api.delete(iti.issue_tracked_obj)
    mock_update_issue.assert_called_with(iti.issue_id, expected_query)
