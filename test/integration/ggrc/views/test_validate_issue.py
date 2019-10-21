# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test `validate_issue` endpoint."""

import ddt
import mock

from ggrc import settings
from ggrc.integrations import constants as integration_constants
from ggrc.integrations import integrations_errors
from integration import ggrc
from integration.ggrc import api_helper
from integration.ggrc.models import factories


@ddt.ddt
@mock.patch.object(settings, "ISSUE_TRACKER_ENABLED", True)
@mock.patch('ggrc.integrations.issues.Client.get_issue',
            return_value=mock.MagicMock())
class TestWithValidateIssue(ggrc.TestCase):
  """Tests for `validate_issue` endpoint."""

  URL = "/api/validate_issue/{issue_id}"

  def setUp(self):
    super(TestWithValidateIssue, self).setUp()
    self.api = api_helper.Api()
    self.api.client.get("/login")

  @ddt.data(
      factories.AssessmentFactory,
      factories.IssueFactory,
  )
  def test_no_access(self, factory, get_issue_mock):
    """Test if there is no access to issue or issue does not exist."""
    get_issue_mock.side_effect = integrations_errors.Error
    with factories.single_commit():
      linked_resource = factory()
      issuetracker_issue = factories.IssueTrackerIssueFactory(
          issue_tracked_obj=linked_resource,
      )

    response = self.api.client.get(
        self.URL.format(issue_id=issuetracker_issue.id),
    )

    self.assert200(response)
    self.assertEqual(
        response.json,
        {
            "msg": integration_constants.TICKET_NO_ACCESS_TMPL,
            "valid": False,
            "type": None,
            "id": None,
        })

  @ddt.data(
      factories.AssessmentFactory,
      factories.IssueFactory,
  )
  def test_already_linked(self, linked_res_factory, get_issue_mock):
    """Test if issue is already linked to GGRC object."""
    get_issue_mock.return_value = {}
    with factories.single_commit():
      linked_resource = linked_res_factory()
      linked_resource_id = linked_resource.id
      issuetracker_issue = factories.IssueTrackerIssueFactory(
          issue_tracked_obj=linked_resource,
      )

    response = self.api.client.get(
        self.URL.format(issue_id=issuetracker_issue.issue_id),
    )

    self.assert200(response)
    self.assertEqual(
        response.json,
        {
            "msg": integration_constants.TICKET_ALREADY_LINKED_TMPL,
            "valid": False,
            "type": linked_resource.type,
            "id": linked_resource_id,
        })

  def test_exist_not_linked(self, get_issue_mock):
    """Test if issue exists and is not linked to GGRC object."""
    get_issue_mock.return_value = {}

    response = self.api.client.get(
        self.URL.format(issue_id=1),
    )

    self.assert200(response)
    self.assertEqual(
        response.json,
        {
            "msg": "",
            "valid": True,
            "type": None,
            "id": None,
        })
