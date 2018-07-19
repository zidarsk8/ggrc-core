# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Integration test for Issu object sync cron job."""

# pylint: disable=protected-access
# pylint: disable=invalid-name


import ddt
import mock
import flask

from ggrc.models import all_models
from ggrc.integrations.synchronization_jobs import issue_sync_job
from ggrc.integrations.synchronization_jobs import sync_utils
from integration import ggrc
from integration.ggrc.models import factories
from api_search.helpers import create_rand_person


@ddt.ddt
class TestIssueIntegration(ggrc.TestCase):
  """Test crom job for sync Issue object attributes."""

  def setUp(self):
    super(TestIssueIntegration, self).setUp()
    self.verifier = factories.PersonFactory()
    self.assignee = factories.PersonFactory()

  @ddt.data(
      ("new", "Draft"),
      ("assigned", "Draft"),
      ("accepted", "Active"),
      ("fixed", "Fixed"),
      ("verified", "Fixed and Verified"),
      ("not_reproducible", "Deprecated"),
      ("intended_behavior", "Deprecated"),
      ("obsolete", "Deprecated"),
      ("infeasible", "Deprecated"),
      ("duplicate", "Deprecated",)
  )
  @ddt.unpack
  def test_sync_issue_statuses(self, issuetracker_status, issue_status):
    """Test updating issue statuses in GGRC."""
    # Arrange test data.
    issue_tracker_issue_id = "1"
    iti = factories.IssueTrackerIssueFactory(
        enabled=True,
        issue_id=issue_tracker_issue_id,
        issue_tracked_obj=factories.IssueFactory(status="Draft")
    )

    batches = [
        {
            issue_tracker_issue_id: {
                "status": issuetracker_status,
                "type": "BUG",
                "priority": "P2",
                "severity": "S2",
            }
        }
    ]

    # Perform action.
    with mock.patch.object(sync_utils, "iter_issue_batches",
                           return_value=batches):
      issue_sync_job.sync_issue_attributes()

    # Assert results.
    issue = all_models.Issue.query.get(iti.issue_tracked_obj.id)
    self.assertEquals(issue.status, issue_status)

  def initialize_test_issuetracker_info(self):
    """Create Issue with admin and primary contact"""
    iti = factories.IssueTrackerIssueFactory(
        enabled=True,
        issue_id="1",
        issue_tracked_obj=factories.IssueFactory(status="Draft")
    )

    # Add Admin into issue.
    admin_role = all_models.AccessControlRole.query.filter_by(
        object_type=all_models.Issue.__name__, name="Admin"
    ).first()
    factories.AccessControlListFactory(
        ac_role=admin_role,
        object=iti.issue_tracked_obj,
        person=self.verifier
    )

    # Add primary contact into issue.
    primary_contact_role = all_models.AccessControlRole.query.filter_by(
        object_type=all_models.Issue.__name__, name="Primary Contacts"
    ).first()
    factories.AccessControlListFactory(
        ac_role=primary_contact_role,
        object=iti.issue_tracked_obj,
        object_id=iti.issue_tracked_obj.id,
        person=self.assignee,
    )

    return iti

  def test_sync_verifier_email(self):
    """Test adding new verifier email into Issue ACL."""
    # Arrange test data.
    new_verifier = create_rand_person()
    iti = self.initialize_test_issuetracker_info()

    batches = [
        {
            "1": {
                "status": "NEW",
                "type": "BUG",
                "priority": "P2",
                "severity": "S2",
                "verifier": new_verifier.email,
                "assignee": self.assignee.email,
            }
        }
    ]

    # Perform action.
    with mock.patch.object(flask, "g"):
      with mock.patch.object(sync_utils, "iter_issue_batches",
                             return_value=batches):
        issue_sync_job.sync_issue_attributes()

      # Assert results.
      issue = all_models.Issue.query.get(iti.issue_tracked_obj.id)
      admin_emails = [
          person.email for person in issue.get_persons_for_rolename("Admin")
      ]
      self.assertListEqual(
          admin_emails,
          [self.verifier.email, new_verifier.email]
      )

      primary_contacts_emails = [
          person.email
          for person in issue.get_persons_for_rolename("Primary Contacts")
      ]
      self.assertListEqual(primary_contacts_emails, [self.assignee.email])

  def test_sync_assignee_email(self):
    """Test adding new assignee email into Issue ACL."""
    # Arrange test data.
    new_assignee = create_rand_person()
    iti = self.initialize_test_issuetracker_info()

    batches = [
        {
            "1": {
                "status": "NEW",
                "type": "BUG",
                "priority": "P2",
                "severity": "S2",
                "verifier": self.verifier.email,
                "assignee": new_assignee.email,
            }
        }
    ]

    # Perform action.
    with mock.patch.object(flask, "g"):
      with mock.patch.object(sync_utils, "iter_issue_batches",
                             return_value=batches):
        issue_sync_job.sync_issue_attributes()

      issue = all_models.Issue.query.get(iti.issue_tracked_obj.id)

      # Check unchanged admins
      admin_emails = [
          person.email for person in issue.get_persons_for_rolename("Admin")
      ]
      self.assertListEqual(admin_emails, [self.verifier.email, ])

      # Check changed primary contacts
      primary_contacts_emails = [
          person.email
          for person in issue.get_persons_for_rolename("Primary Contacts")
      ]
      self.assertListEqual(
          primary_contacts_emails,
          [self.assignee.email, new_assignee.email]
      )
