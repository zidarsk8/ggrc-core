# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

# pylint: disable=maybe-no-member, invalid-name

"""Test Issue import and updates."""

from collections import OrderedDict

from ggrc import models
from ggrc.converters import errors

from integration.ggrc.models import factories
from integration.ggrc import TestCase


class TestImportIssues(TestCase):
  """Basic Issue import tests."""

  def setUp(self):
    """Set up for Issue test cases."""
    super(TestImportIssues, self).setUp()
    self.client.get("/login")

  def test_basic_issue_import(self):
    """Test basic issue import."""
    audit = factories.AuditFactory()
    for i in range(2):
      response = self.import_data(OrderedDict([
          ("object_type", "Issue"),
          ("Code*", ""),
          ("Title*", "Test issue {}".format(i)),
          ("Admin*", "user@example.com"),
          ("audit", audit.slug),
      ]))
      self._check_csv_response(response, {})

    for issue in models.Issue.query:
      self.assertIsNotNone(
          models.Relationship.find_related(issue, audit),
          "Could not find relationship between: {} and {}".format(
              issue.slug, audit.slug)
      )

  def test_audit_change(self):
    """Test audit changing"""
    audit = factories.AuditFactory()
    issue = factories.IssueFactory()
    response = self.import_data(OrderedDict([
        ("object_type", "Issue"),
        ("Code*", issue.slug),
        ("audit", audit.slug),
    ]))
    self._check_csv_response(response, {
        "Issue": {
            "row_warnings": {
                errors.UNMODIFIABLE_COLUMN.format(line=3, column_name="Audit")
            }
        }
    })

  def test_import_with_mandatory(self):
    """Test import of data with mandatory role"""
    # Import of data should be allowed if mandatory role provided
    # and can process situation when nonmandatory roles are absent
    # without any errors and warnings
    mandatory_role = factories.AccessControlRoleFactory(
        object_type="Market",
        mandatory=True
    ).name
    factories.AccessControlRoleFactory(
        object_type="Market",
        mandatory=False
    ).name

    email = factories.PersonFactory().email
    response_json = self.import_data(OrderedDict([
        ("object_type", "Market"),
        ("code", "market-1"),
        ("title", "Title"),
        ("Admin", "user@example.com"),
        (mandatory_role, email),
    ]))
    self._check_csv_response(response_json, {})
    self.assertEqual(1, response_json[0]["created"])
    self.assertEqual(1, len(models.Market.query.all()))

  def test_import_without_mandatory(self):
    """Test import of data without mandatory role"""
    # Data can't be imported if mandatory role is not provided
    mandatory_role = factories.AccessControlRoleFactory(
        object_type="Market",
        mandatory=True
    ).name
    not_mandatory_role = factories.AccessControlRoleFactory(
        object_type="Market",
        mandatory=False
    ).name

    email = factories.PersonFactory().email
    response_json = self.import_data(OrderedDict([
        ("object_type", "Market"),
        ("code", "market-1"),
        ("title", "Title"),
        ("Admin", "user@example.com"),
        (not_mandatory_role, email),
    ]))

    expected_errors = {
        errors.MISSING_COLUMN.format(
            line=3, column_names=mandatory_role, s=""
        ),
    }
    response_errors = response_json[0]["row_errors"]
    self.assertEqual(expected_errors, set(response_errors))
    response_warnings = response_json[0]["row_warnings"]
    self.assertEqual(set(), set(response_warnings))
    self.assertEqual(0, response_json[0]["created"])

    markets = models.Market.query.all()
    self.assertEqual(len(markets), 0)
