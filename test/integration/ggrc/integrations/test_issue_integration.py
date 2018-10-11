# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Integration tests for Issue with IssueTracker integration."""

# pylint: disable=unused-argument

import mock
import ddt

from ggrc import db
from ggrc import models
from ggrc import settings
from ggrc.models import all_models
from ggrc.models.hooks.issue_tracker import integration_utils
from ggrc.models.hooks.issue_tracker import issue_tracker_params_builder \
    as params_builder
from ggrc.integrations import integrations_errors
from ggrc.integrations.synchronization_jobs.issue_sync_job import \
    ISSUE_STATUS_MAPPING

from integration.ggrc.models import factories
from integration import ggrc
from integration.ggrc.api_helper import Api

TICKET_ID = 123


@ddt.ddt
class TestIssueIntegration(ggrc.TestCase):
  """Test set for IssueTracker integration functionality."""
  DEFAULT_ISSUE_ATTRS = {
      "title": "title1",
      "context": None,
      "status": "Draft",
      "enabled": True,
      "component_id": 1234,
      "hotlist_id": 4321,
      "issue_id": TICKET_ID,
      "issue_type": "Default Issue Type",
      "issue_priority": "P2",
      "issue_severity": "S1",
  }

  DEFAULT_TICKET_ATTRS = {
      "component_id": 1234,
      "hotlist_id": 4321,
      "issue_id": TICKET_ID,
      "status": "new",
      "issue_type": "Default Issue type",
      "issue_priority": "P1",
      "issue_severity": "S2",
      "title": "test title",
      "verifier": "user@example.com",
      "assignee": "user@example.com",
      "ccs": ["user@example.com"],
  }

  # pylint: disable=invalid-name

  def setUp(self):
    # pylint: disable=super-on-old-class
    super(TestIssueIntegration, self).setUp()
    self.api = Api()
    self.client.get("/login")

  @mock.patch("ggrc.integrations.issues.Client.create_issue",
              return_value={"issueId": "issueId"})
  @mock.patch.object(settings, "ISSUE_TRACKER_ENABLED", True)
  def test_create_issue_tracker_info(self, mock_create_issue):
    """Test creation issue tracker issue for Issue object."""
    component_id = "1234"
    hotlist_id = "4321"
    issue_type = "Default Issue type"
    issue_priority = "P2"
    issue_severity = "S1"
    title = "test title"

    with mock.patch.object(integration_utils, "exclude_auditor_emails",
                           return_value={u"user@example.com", }):
      response = self.api.post(all_models.Issue, {
          "issue": {
              "title": title,
              "context": None,
              "issue_tracker": {
                  "enabled": True,
                  "component_id": int(component_id),
                  "hotlist_id": int(hotlist_id),
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
      self.assertEqual(issue_tracker_issue.title, title)
      self.assertEqual(issue_tracker_issue.component_id, component_id)
      self.assertEqual(issue_tracker_issue.hotlist_id, hotlist_id)
      self.assertEqual(issue_tracker_issue.issue_type, issue_type)
      self.assertEqual(issue_tracker_issue.issue_priority, issue_priority)
      self.assertEqual(issue_tracker_issue.issue_severity, issue_severity)

  def test_exclude_auditor(self):
    """Test 'exclude_auditor_emails' util."""
    audit = factories.AuditFactory()
    person = factories.PersonFactory(email="auditor@example.com")
    audit.add_person_with_role_name(person, "Auditors")
    db.session.commit()

    result = integration_utils.exclude_auditor_emails(["auditor@example.com",
                                                       "admin@example.com"])
    self.assertEqual(result, {"admin@example.com", })

  @ddt.data(
      ({"description": "new description"},
       {"comment": "Issue Description has been updated.\nnew description"}),
      ({"test_plan": "new test plan"},
       {"comment": "Issue Remediation Plan has been updated.\nnew test plan"}),
      ({"issue_tracker": {"component_id": "123",
                          "enabled": True,
                          "issue_id": TICKET_ID}},
       {"component_id": 123}),
      ({"issue_tracker": {"hotlist_id": "321",
                          "enabled": True,
                          "issue_id": TICKET_ID}},
       {"hotlist_ids": [321, ]}),
      ({"issue_tracker": {"issue_priority": "P2",
                          "enabled": True,
                          "issue_id": TICKET_ID}},
       {"priority": "P2"}),
      ({"issue_tracker": {"issue_severity": "S2",
                          "enabled": True,
                          "issue_id": TICKET_ID}},
       {"severity": "S2"}),
      ({"issue_tracker": {"enabled": False,
                          "hotlist_ids": [999, ],
                          "issue_id": TICKET_ID}},
       {"comment": "Changes to this GGRC object will no longer be "
                   "tracked within this bug."}),
  )
  @ddt.unpack
  @mock.patch("ggrc.integrations.issues.Client.update_issue")
  def test_update_issue(self, issue_attrs, expected_query, mock_update_issue):
    """Test updating issue tracker issue."""
    iti = factories.IssueTrackerIssueFactory(
        enabled=True,
        issue_id=TICKET_ID,
        issue_tracked_obj=factories.IssueFactory()
    )

    with mock.patch.object(settings, "ISSUE_TRACKER_ENABLED", True):
      self.api.put(iti.issue_tracked_obj, issue_attrs)
    mock_update_issue.assert_called_with(iti.issue_id, expected_query)

  @ddt.data(
      {"notes": "new notes"},
      {"end_date": "2018-07-15"},
      {"start_date": "2018-07-15"},
  )
  @mock.patch("ggrc.integrations.issues.Client.update_issue")
  def test_update_issue_with_untracked_fields(self, issue_attrs,
                                              mock_update_issue):
    """Test updating issue with fields which shouldn't be sync."""
    iti = factories.IssueTrackerIssueFactory(
        enabled=True,
        issue_tracked_obj=factories.IssueFactory()
    )
    with mock.patch.object(settings, "ISSUE_TRACKER_ENABLED", True):
      self.api.put(iti.issue_tracked_obj, issue_attrs)
    mock_update_issue.assert_not_called()

  def request_payload_builder(self, issue_attrs):
    """Build payload for POST request to Issue Tracker"""
    payload_attrs = dict(self.DEFAULT_ISSUE_ATTRS, **issue_attrs)
    payload = {"issue": {
        "title": payload_attrs["title"],
        "context": payload_attrs["context"],
        "status": payload_attrs["status"],
        "issue_tracker": {
            "enabled": payload_attrs["enabled"],
            "component_id": payload_attrs["component_id"],
            "hotlist_id": payload_attrs["hotlist_id"],
            "issue_id": payload_attrs["issue_id"],
            "issue_type": payload_attrs["issue_type"],
            "issue_priority": payload_attrs["issue_priority"],
            "issue_severity": payload_attrs["issue_severity"],
            "title": payload_attrs["title"],
        }
    }}
    return payload

  def put_request_payload_builder(self, issue_attrs):
    """Build payload for PUT request to Issue Tracker"""
    payload_attrs = dict(self.DEFAULT_ISSUE_ATTRS, **issue_attrs)
    payload = {
        "issue_tracker": {
            "enabled": payload_attrs["enabled"],
            "component_id": payload_attrs["component_id"],
            "hotlist_id": payload_attrs["hotlist_id"],
            "issue_id": payload_attrs["issue_id"],
            "issue_type": payload_attrs["issue_type"],
            "issue_priority": payload_attrs["issue_priority"],
            "issue_severity": payload_attrs["issue_severity"],
            "title": payload_attrs["title"],
        }
    }
    return payload

  def response_payload_builder(self, ticket_attrs):
    """Build payload for response from Issue Tracker via get_issue method"""
    payload_attrs = dict(self.DEFAULT_TICKET_ATTRS, **ticket_attrs)
    payload = {"issueState": {
        "component_id": payload_attrs["component_id"],
        "hotlist_id": payload_attrs["hotlist_id"],
        "issue_id": payload_attrs["issue_id"],
        "status": payload_attrs["status"],
        "issue_type": payload_attrs["issue_type"],
        "issue_priority": payload_attrs["issue_priority"],
        "issue_severity": payload_attrs["issue_severity"],
        "title": payload_attrs["title"],
        "verifier": payload_attrs["verifier"],
        "assignee": payload_attrs["assignee"],
        "ccs": payload_attrs["ccs"],
    }}
    return payload

  def check_issuetracker_issue_fields(self,
                                      obj,
                                      issue_tracker_issue,
                                      issue_attrs,
                                      issue_tracker_ticket_attrs):
    """Checks issuetracker_issue were updated correctly.

    Make assertions to check if issue tracker fields were updated according
    our business logic.
    For Issue model we should get title, component_id, hotlist_id,
    priority, severity, issue_id and issue_type from GGRC and status from
    Issue Tracker.
    """

    self.assertTrue(issue_tracker_issue.enabled)

    # According to our business logic these attributes should be taken
    # from issue information
    self.assertEqual(issue_tracker_issue.title,
                     issue_attrs["issue"]["title"])
    self.assertEqual(int(issue_tracker_issue.component_id),
                     issue_attrs["issue"]["issue_tracker"]["component_id"])
    self.assertEqual(int(issue_tracker_issue.hotlist_id),
                     issue_attrs["issue"]["issue_tracker"]["hotlist_id"])
    self.assertEqual(issue_tracker_issue.issue_priority,
                     issue_attrs["issue"]["issue_tracker"]["issue_priority"])
    self.assertEqual(issue_tracker_issue.issue_severity,
                     issue_attrs["issue"]["issue_tracker"]["issue_severity"])
    self.assertEqual(int(issue_tracker_issue.issue_id),
                     issue_attrs["issue"]["issue_tracker"]["issue_id"])
    self.assertEqual(issue_tracker_issue.issue_type,
                     issue_attrs["issue"]["issue_tracker"]["issue_type"])

    # These attributes should be taken from ticket information
    ticket_status = issue_tracker_ticket_attrs["issueState"]["status"]
    ticket_mapped_status = ISSUE_STATUS_MAPPING[ticket_status]
    self.assertEqual(obj.status, ticket_mapped_status)

  @ddt.data(
      ({"title": "first_title"}, {"title": "other_title"}),
      ({"issue_type": "type1"}, {"issue_type": "process"}),
      ({"issue_severity": "S0"}, {"issue_severity": "S1"}),
      ({"issue_priority": "P0"}, {"issue_priority": "P1"}),
      ({"hotlist_id": 1234}, {"hotlist_id": 4321}),
      ({"component_id": 1234}, {"component_id": 4321}),
      ({"status": "Draft"}, {"status": "fixed"}),
  )
  @ddt.unpack
  @mock.patch("ggrc.integrations.issues.Client.update_issue")
  @mock.patch.object(settings, "ISSUE_TRACKER_ENABLED", True)
  def test_new_issue_linking(self, issue_attrs, ticket_attrs, update_mock):
    """Test linking new Issue to IssueTracker ticket sets correct fields"""
    issue_request_payload = self.request_payload_builder(issue_attrs)
    response_payload = self.response_payload_builder(ticket_attrs)
    with mock.patch("ggrc.integrations.issues.Client.get_issue",
                    return_value=response_payload) as get_mock:
      with mock.patch.object(integration_utils, "exclude_auditor_emails",
                             return_value={u"user@example.com", }):
        response = self.api.post(all_models.Issue, issue_request_payload)
      get_mock.assert_called_once()
    update_mock.assert_called_once()

    self.assertEqual(response.status_code, 201)
    issue_id = response.json.get("issue").get("id")
    issue_tracker_issue = models.IssuetrackerIssue.get_issue("Issue", issue_id)
    issue = all_models.Issue.query.filter_by(id=issue_id).first()
    self.check_issuetracker_issue_fields(issue,
                                         issue_tracker_issue,
                                         issue_request_payload,
                                         response_payload)

  @mock.patch("ggrc.integrations.issues.Client.update_issue")
  @mock.patch.object(settings, "ISSUE_TRACKER_ENABLED", True)
  def test_people_merge_after_linking(self, update_mock):
    """Test people roles were updated while linking new ticket"""
    ticket_attrs = {
        "verifier": "verifier@example.com",
        "assignee": "assignee@example.com",
        "ccs": ["cc1@example.com", "cc2@example.com"],
    }

    with factories.single_commit():
      factories.PersonFactory(email="verifier@example.com")
      factories.PersonFactory(email="assignee@example.com")
      for email in ["cc1@example.com", "cc2@example.com"]:
        factories.PersonFactory(email=email)

    issue_request_payload = self.request_payload_builder({})
    response_payload = self.response_payload_builder(ticket_attrs)
    with mock.patch("ggrc.integrations.issues.Client.get_issue",
                    return_value=response_payload) as get_mock:
      with mock.patch.object(integration_utils, "exclude_auditor_emails",
                             return_value={u"user@example.com", }):
        response = self.api.post(all_models.Issue, issue_request_payload)
      get_mock.assert_called_once()
    update_mock.assert_called_once()

    self.assertEqual(response.status_code, 201)
    issue_id = response.json.get("issue").get("id")
    issue = all_models.Issue.query.filter_by(id=issue_id).first()

    admins = [person.email for person
              in issue.get_persons_for_rolename("Admin")]
    primary = [person.email for person
               in issue.get_persons_for_rolename("Primary Contacts")]
    secondary = [person.email for person
                 in issue.get_persons_for_rolename("Secondary Contacts")]
    # assert ticket roles were added to Issue
    self.assertIn("verifier@example.com", admins)
    self.assertIn("assignee@example.com", primary)
    for person in ["cc1@example.com", "cc2@example.com"]:
      self.assertIn(person, secondary)

  @mock.patch("ggrc.integrations.issues.Client.update_issue")
  @mock.patch.object(settings, "ISSUE_TRACKER_ENABLED", True)
  def test_existing_issue_link(self, update_mock):
    """Test Issue link to another ticket """
    iti = factories.IssueTrackerIssueFactory(
        enabled=True,
        issue_id=TICKET_ID,
        issue_tracked_obj=factories.IssueFactory()
    )
    new_ticket_id = TICKET_ID + 1
    new_data = {"issue_id": new_ticket_id}
    issue_request_payload = self.put_request_payload_builder(new_data)
    response_payload = self.response_payload_builder(new_data)

    with mock.patch("ggrc.integrations.issues.Client.get_issue",
                    return_value=response_payload) as get_mock:
      with mock.patch.object(integration_utils, "exclude_auditor_emails",
                             return_value={u"user@example.com", }):
        response = self.api.put(iti.issue_tracked_obj, issue_request_payload)
      get_mock.assert_called_once()

    self.assert200(response)

    # check if data was changed in our DB
    issue_id = response.json.get("issue").get("id")
    issue_tracker_issue = models.IssuetrackerIssue.get_issue("Issue", issue_id)
    self.assertEqual(int(issue_tracker_issue.issue_id), new_ticket_id)

    # check detach comment was sent
    detach_comment_template = params_builder.IssueParamsBuilder.DETACH_TMPL
    comment = detach_comment_template.format(new_ticket_id=new_ticket_id)
    expected_args = (TICKET_ID, {"comment": comment})
    self.assertEqual(expected_args, update_mock.call_args[0])

  @mock.patch.object(settings, "ISSUE_TRACKER_ENABLED", True)
  def test_already_linked_ticket(self):
    """Test Issue without IT couldn't be linked to already linked ticket"""
    with factories.single_commit():
      factories.IssueTrackerIssueFactory(
          enabled=True,
          issue_id=TICKET_ID,
          issue_tracked_obj=factories.IssueFactory()
      )
      new_issue = factories.IssueFactory()

    issue_data = {"issue_id": TICKET_ID}
    issue_request_payload = self.put_request_payload_builder(issue_data)

    response = self.api.put(new_issue, issue_request_payload)
    self.assert200(response)
    self.assertTrue(response.json["issue"]["issue_tracker"]["_warnings"])
    issue_id = response.json.get("issue").get("id")
    issue_tracker_issue = models.IssuetrackerIssue.get_issue("Issue", issue_id)
    self.assertFalse(issue_tracker_issue)

  @mock.patch("ggrc.integrations.issues.Client.update_issue")
  @mock.patch.object(settings, "ISSUE_TRACKER_ENABLED", True)
  def test_creating_new_ticket_for_linked_issue(self, update_mock):
    """Test create new ticket for already linked issue"""
    iti = factories.IssueTrackerIssueFactory(
        enabled=True,
        issue_id=TICKET_ID,
        issue_tracked_obj=factories.IssueFactory()
    )
    new_data = {"issue_id": ''}
    issue_request_payload = self.put_request_payload_builder(new_data)

    with mock.patch.object(integration_utils, "exclude_auditor_emails",
                           return_value={u"user@example.com", }):
      with mock.patch("ggrc.integrations.issues.Client.create_issue",
                      return_value={"issueId": TICKET_ID + 1}) as create_mock:
        response = self.api.put(iti.issue_tracked_obj, issue_request_payload)

    self.assert200(response)

    # Detach comment should be sent to previous ticket
    update_mock.assert_called_once()
    self.assertEqual(TICKET_ID, update_mock.call_args[0][0])
    create_mock.assert_called_once()

    # check if data was changed in our DB
    issue_id = response.json.get("issue").get("id")
    issue_tracker_issue = models.IssuetrackerIssue.get_issue("Issue", issue_id)
    self.assertNotEqual(int(issue_tracker_issue.issue_id), TICKET_ID)

  @mock.patch("ggrc.integrations.issues.Client.update_issue")
  def test_issue_tracker_error(self, update_issue_mock):
    """Test that issue tracker does not change state
       in case receiving an error."""
    iti = factories.IssueTrackerIssueFactory(
        enabled=True,
        issue_tracked_obj=factories.IssueFactory()
    )
    update_issue_mock.side_effect = integrations_errors.HttpError("data")
    issue_attrs = {
        "issue_tracker": {
            "enabled": True,
            "hotlist_id": "123",
            "issue_id": iti.issue_id,

        }
    }
    with mock.patch.object(settings, "ISSUE_TRACKER_ENABLED", True),\
        mock.patch.object(all_models.IssuetrackerIssue,
                          "create_or_update_from_dict") as update_info_mock:
      self.api.put(iti.issue_tracked_obj, issue_attrs)

    # Check that "enabled" flag hasn't been changed.
    self.assertTrue("enabled" not in update_info_mock.call_args[0][1])

  @mock.patch("ggrc.integrations.issues.Client.update_issue")
  def test_delete_issue(self, mock_update_issue):
    """Test updating issue tracker issue when issue in GGRC has been deleted"""
    iti = factories.IssueTrackerIssueFactory(
        enabled=True,
        issue_tracked_obj=factories.IssueFactory()
    )
    expected_query = {"comment": "GGRC object has been deleted. GGRC changes "
                                 "will no longer be tracked within this bug."}
    with mock.patch.object(settings, "ISSUE_TRACKER_ENABLED", True):
      self.api.delete(iti.issue_tracked_obj)
    mock_update_issue.assert_called_with(iti.issue_id, expected_query)

  @mock.patch.object(params_builder.BaseIssueTrackerParamsBuilder,
                     "get_ggrc_object_url",
                     return_value="http://issue_url.com")
  @mock.patch("ggrc.integrations.issues.Client.update_issue")
  def test_adding_comment_to_issue(self, update_issue_mock, url_builder_mock):
    """Test adding comment to issue."""
    # TODO: this test depends on outer scope. Different username
    # in different calls
    iti = factories.IssueTrackerIssueFactory(
        enabled=True,
        issue_tracked_obj=factories.IssueFactory()
    )
    comment = factories.CommentFactory(description="test comment")

    expected_result = {
        "comment": u"A new comment is added by 'Example User' to the"
                   u" 'Issue': 'test comment'.\n"
                   u"Use the following to link to get more "
                   u"information from the GGRC 'Issue'. Link - "
                   u"http://issue_url.com"
    }

    with mock.patch.object(settings, "ISSUE_TRACKER_ENABLED", True):
      self.api.post(all_models.Relationship, {
          "relationship": {
              "source": {"id": iti.issue_tracked_obj.id, "type": "Issue"},
              "destination": {"id": comment.id, "type": "comment"},
              "context": None
          },
      })
    url_builder_mock.assert_called_once()
    update_issue_mock.assert_called_with(iti.issue_id, expected_result)

  @mock.patch("ggrc.integrations.issues.Client.update_issue")
  @mock.patch.object(settings, "ISSUE_TRACKER_ENABLED", True)
  def test_mapping_document(self, update_issue_mock):
    """Test map document action on issue.

    Issue in Issue tracker shouldn't be updated when reference url has been
    added to issue.
    """
    iti = factories.IssueTrackerIssueFactory(
        enabled=True,
        issue_tracked_obj=factories.IssueFactory()
    )
    document = factories.DocumentFactory()
    response = self.api.put(
        iti.issue_tracked_obj,
        {
            "actions": {
                "add_related": [{"id": document.id, "type": "Document", }, ]
            }
        }
    )
    self.assert200(response)

    relationship = all_models.Relationship.query.filter(
        all_models.Relationship.source_type == "Issue",
        all_models.Relationship.source_id == response.json["issue"]["id"],
    ).order_by(all_models.Relationship.id.desc()).first()

    self.assertEqual(relationship.destination_id, document.id)
    self.assertEqual(relationship.source_id, iti.issue_tracked_obj.id)

    # Check that issue in Issue Tracker hasn't been updated.
    update_issue_mock.assert_not_called()


@ddt.ddt
class TestDisabledIssueIntegration(ggrc.TestCase):
  """Tests for IssueTracker integration functionality with disabled sync."""

  # pylint: disable=invalid-name

  def setUp(self):
    # pylint: disable=super-on-old-class
    super(TestDisabledIssueIntegration, self).setUp()
    self.api = Api()
    self.client.get("/login")

  @mock.patch("ggrc.integrations.issues.Client.create_issue")
  def test_issue_creation(self, mock_create_issue):
    """Test creating Issue object with disabled integration."""
    with mock.patch.object(settings, "ISSUE_TRACKER_ENABLED", True):
      response = self.api.post(all_models.Issue, {
          "issue": {
              "title": "test title",
              "context": None,
              "issue_tracker": {
                  "enabled": False,
              }
          },
      })
    mock_create_issue.assert_not_called()
    self.assertEqual(response.status_code, 201)
    issue_id = response.json.get("issue").get("id")
    issue_tracker_issue = models.IssuetrackerIssue.get_issue("Issue",
                                                             issue_id)
    self.assertIsNone(issue_tracker_issue)

  @mock.patch("ggrc.integrations.issues.Client.update_issue")
  def test_issue_deletion(self, mock_update_issue):
    """Test deleting Issue object with disabled integration for issue."""
    iti = factories.IssueTrackerIssueFactory(
        enabled=False,
        issue_tracked_obj=factories.IssueFactory()
    )
    with mock.patch.object(settings, "ISSUE_TRACKER_ENABLED", True):
      self.api.delete(iti.issue_tracked_obj)
    mock_update_issue.assert_not_called()

  @ddt.data(
      {"description": "new description",
       "issue_tracker": {"issue_id": TICKET_ID, "enabled": False}},
      {"test_plan": "new test plan",
       "issue_tracker": {"issue_id": TICKET_ID, "enabled": False}},
      {"issue_tracker": {"issue_id": TICKET_ID,
                         "component_id": "123",
                         "enabled": False}},
      {"issue_tracker": {"issue_id": TICKET_ID,
                         "hotlist_id": "321",
                         "enabled": False}},
      {"issue_tracker": {"issue_id": TICKET_ID,
                         "issue_priority": "P2",
                         "enabled": False}},
      {"issue_tracker": {"issue_id": TICKET_ID,
                         "issue_severity": "S2",
                         "enabled": False}},
  )
  @mock.patch("ggrc.integrations.issues.Client.update_issue")
  def test_update_issue_object(self, issue_attrs, mock_update_issue):
    """Test updating issue object with disabled integration for issue."""
    iti = factories.IssueTrackerIssueFactory(
        enabled=False,
        issue_id=TICKET_ID,
        issue_tracked_obj=factories.IssueFactory()
    )
    with mock.patch.object(settings, "ISSUE_TRACKER_ENABLED", True):
      self.api.put(iti.issue_tracked_obj, issue_attrs)
    mock_update_issue.assert_not_called()

  @mock.patch("ggrc.integrations.issues.Client.create_issue",
              side_effect=[integrations_errors.Error, {"issueId": "issueId"}])
  @mock.patch.object(settings, "ISSUE_TRACKER_ENABLED", True)
  def test_issue_recreation(self, mock_create_issue):
    """Test retrying to turn on integration after failed creation."""
    # Arrange data.
    component_id = "1234"
    hotlist_id = "4321"
    issue_type = "Default Issue type"
    issue_priority = "P2"
    issue_severity = "S1"
    title = "test title"
    issue_tracker_attrs = {
        "enabled": True,
        "component_id": int(component_id),
        "hotlist_id": int(hotlist_id),
        "issue_type": issue_type,
        "issue_priority": issue_priority,
        "issue_severity": issue_severity,
    }

    # Perform actions and assert results.
    with mock.patch.object(integration_utils, "exclude_auditor_emails",
                           return_value={u"user@example.com", }):

      # Try to create issue. create_issue should raise exception here.
      response = self.api.post(all_models.Issue, {
          "issue": {
              "title": title,
              "context": None,
              "issue_tracker": issue_tracker_attrs
          },
      })

      issue_id = response.json.get("issue").get("id")
      issue_tracker_issue = models.IssuetrackerIssue.get_issue("Issue",
                                                               issue_id)
      self.assertIsNone(issue_tracker_issue.issue_id)
      self.assertIsNone(issue_tracker_issue.issue_url)

      # Try to turn on integration on already created issue.
      self.api.put(
          issue_tracker_issue.issue_tracked_obj,
          {"issue_tracker": issue_tracker_attrs}
      )

      issue_id = issue_tracker_issue.issue_tracked_obj.id
      issue_tracker_issue = models.IssuetrackerIssue.get_issue("Issue",
                                                               issue_id)
      self.assertEqual(issue_tracker_issue.issue_url, "http://issue/issueId")

  @mock.patch("ggrc.integrations.issues.Client.update_issue")
  def test_adding_comment_to_issue(self, update_issue_mock):
    """Test not adding comment to issue when issue tracker disabled."""
    iti = factories.IssueTrackerIssueFactory(
        enabled=False,
        issue_tracked_obj=factories.IssueFactory()
    )
    comment = factories.CommentFactory(description="test comment")

    with mock.patch.object(settings, "ISSUE_TRACKER_ENABLED", True):
      self.api.post(all_models.Relationship, {
          "relationship": {
              "source": {"id": iti.issue_tracked_obj.id, "type": "Issue"},
              "destination": {"id": comment.id, "type": "comment"},
              "context": None
          },
      })
    update_issue_mock.assert_not_called()
