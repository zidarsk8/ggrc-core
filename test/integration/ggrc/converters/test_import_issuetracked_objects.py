# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Integration tests for IssueTracker updates via import cases."""

# pylint: disable=invalid-name

from collections import OrderedDict

import ddt
import mock

from ggrc import settings, models
from ggrc.models import all_models
from ggrc.models.hooks.issue_tracker import assessment_integration
from ggrc.converters import errors
from ggrc.integrations.constants import DEFAULT_ISSUETRACKER_VALUES as \
    default_values

from integration import ggrc
from integration.ggrc.models import factories
from integration.ggrc.api_helper import Api


@ddt.ddt
class TestIssueTrackedImport(ggrc.TestCase):
  """Test cases for IssueTracker integration via import."""

  def setUp(self):
    # pylint: disable=super-on-old-class
    super(TestIssueTrackedImport, self).setUp()
    self.api = Api()
    self.client.get("/login")

  @mock.patch('ggrc.integrations.issues.Client.create_issue')
  def test_asmt_creation_detached(self, mock_create_issue):
    """Test assessment creation via import detached from IssueTracker hooks."""
    with mock.patch.object(assessment_integration, '_is_issue_tracker_enabled',
                           return_value=True):
      self.import_file("assessment_full_no_warnings.csv")
    mock_create_issue.assert_not_called()

  @mock.patch('ggrc.integrations.issues.Client.create_issue')
  @mock.patch.object(settings, "ISSUE_TRACKER_ENABLED", True)
  def test_issue_creation_detached(self, mock_create_issue):
    """Test issue creation via import detached from IssueTracker hooks."""
    self.import_file("issue_for_import.csv")
    mock_create_issue.assert_not_called()

  @ddt.data(
      ("Issue", "component_id", "Component ID", 123),
      ("Issue", "hotlist_id", "Hotlist ID", 321),
      ("Issue", "issue_priority", "Priority", "P1"),
      ("Issue", "issue_severity", "Severity", "S1"),
      ("Issue", "issue_type", "Issue Type", "BUG"),
      ("Issue", "title", "Issue Title", "iti_title"),
      ("Assessment", "component_id", "Component ID", 123),
      ("Assessment", "hotlist_id", "Hotlist ID", 321),
      ("Assessment", "issue_priority", "Priority", "P1"),
      ("Assessment", "issue_severity", "Severity", "S1"),
      ("Assessment", "issue_type", "Issue Type", "BUG"),
      ("Assessment", "title", "Issue Title", "iti_title"),
  )
  @ddt.unpack
  def test_import_update_succeed(self, model, field, alias, value):
    """Test {0} {2} set correctly during update via import."""
    with factories.single_commit():
      factory = factories.get_model_factory(model)
      obj = factory()
      factories.IssueTrackerIssueFactory(
          issue_tracked_obj=obj,
      )

    response = self.import_data(OrderedDict([
        ("object_type", model),
        ("Code*", obj.slug),
        (alias, value),
    ]))
    obj = models.get_model(model).query.one()
    self._check_csv_response(response, {})
    self.assertEqual(str(obj.issue_tracker[field]), str(value))

  @ddt.data(
      ("component_id", "Component ID", 123),
      ("hotlist_id", "Hotlist ID", 321),
      ("issue_priority", "Priority", "P1"),
      ("issue_severity", "Severity", "S1"),
      ("issue_type", "Issue Type", "BUG"),
      ("title", "Issue Title", "iti_title"),
  )
  @ddt.unpack
  def test_issue_import_create_succeed(self, field, alias, value):
    """Test Issue {1} set correctly during create via import."""
    response = self.import_data(OrderedDict([
        ("object_type", "Issue"),
        ("Code*", "OBJ-1"),
        ("Admin", "user@example.com"),
        ("Title", "Object Title"),
        (alias, value),
    ]))

    self._check_csv_response(response, {})
    obj = all_models.Issue.query.one()
    self.assertEqual(str(obj.issue_tracker[field]), str(value))

  @ddt.data(
      ("component_id", "Component ID", 555),
      ("hotlist_id", "Hotlist ID", 444),
      ("issue_priority", "Priority", "P2"),
      ("issue_severity", "Severity", "S2"),
      ("issue_type", "Issue Type", "PROCESS"),
      ("title", "Issue Title", "iti_title"),
  )
  @ddt.unpack
  def test_assmt_import_create_succeed(self, field, alias, value):
    """Test Assessment {1} set correctly during create via import."""
    audit = factories.AuditFactory()
    response = self.import_data(OrderedDict([
        ("object_type", "Assessment"),
        ("Code*", "OBJ-1"),
        ("Audit*", audit.slug),
        ("Assignees*", "user@example.com"),
        ("Creators", "user@example.com"),
        ("Title", "Object Title"),
        (alias, value),
    ]))

    self._check_csv_response(response, {})
    obj = all_models.Assessment.query.one()
    self.assertEqual(str(obj.issue_tracker[field]), str(value))

  @ddt.data(
      ("component_id", "Component ID", ""),
      ("component_id", "Component ID", "sss"),
      ("hotlist_id", "Hotlist ID", ""),
      ("hotlist_id", "Hotlist ID", "aaa"),
      ("issue_priority", "Priority", ""),
      ("issue_priority", "Priority", "P6"),
      ("issue_severity", "Severity", ""),
      ("issue_severity", "Severity", "aa"),
      ("issue_type", "Issue Type", ""),
      ("issue_type", "Issue Type", "PARABOLA"),
  )
  @ddt.unpack
  def test_default_value_set_correctly(self, missed_field, alias, value):
    """Test correct default value was set to {1} during import"""
    expected_warning = (
        errors.WRONG_VALUE_DEFAULT.format(line=3, column_name=alias)
    )
    expected_messages = {
        "Issue": {
            "row_warnings": {expected_warning},
        }
    }
    response = self.import_data(OrderedDict([
        ("object_type", "Issue"),
        ("Code*", "ISSUE-1"),
        ("Admin", "user@example.com"),
        ("Title", "Issue Title"),
        (alias, value),
    ]))
    self._check_csv_response(response, expected_messages)
    issue = all_models.Issue.query.one()
    self.assertEqual(str(issue.issue_tracker[missed_field]),
                     str(default_values[missed_field]))

  @ddt.data("Issue", "Assessment")
  def test_default_value_title(self, model):
    """Test correct default value was set to {0} Issue Title during import"""
    factory = factories.get_model_factory(model)
    obj = factory(title="Object Title")
    expected_warning = (
        errors.WRONG_VALUE_DEFAULT.format(line=3, column_name="Issue Title")
    )
    expected_messages = {
        model: {
            "row_warnings": {expected_warning},
        }
    }
    response = self.import_data(OrderedDict([
        ("object_type", model),
        ("Code*", obj.slug),
        ("Issue Title", ""),
    ]))
    self._check_csv_response(response, expected_messages)
    obj = models.get_model(model).query.one()
    self.assertEqual(obj.issue_tracker["title"], obj.title)
