# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

# pylint: disable=maybe-no-member

"""Test Assessment Template import."""

from ggrc import models
from ggrc.converters import errors
from integration.ggrc import converters


class TestAssessmentTemplatesImport(converters.TestCase):
  """Assessment Template import tests."""

  def setUp(self):
    """Set up for Request test cases."""
    converters.TestCase.setUp(self)
    self.client.get("/login")

  def test_valid_import(self):
    """Test valid import."""
    response = self.import_file("assessment_template_no_warnings.csv")
    response = next(r for r in response if r["name"] == "Assessment Template")

    self.assertEqual(response["rows"], 4)
    self.assertEqual(response["updated"], 0)
    self.assertEqual(response["created"], 4)
    self.assertEqual(response["row_errors"], [])
    self.assertEqual(response["row_warnings"], [])
    self.assertEqual(response["block_errors"], [])
    self.assertEqual(response["block_warnings"], [])

    people = {p.email: p.id for p in models.Person.query.all()}
    template = models.AssessmentTemplate.query \
        .filter(models.AssessmentTemplate.slug == "T-2") \
        .first()

    self.assertEqual(
        template.default_people["verifiers"],
        [people["user3@a.com"], people["user1@a.com"]],
    )

  def test_invalid_import(self):
    """Test invalid import."""
    data = "assessment_template_with_warnings_and_errors.csv"
    response = self.import_file(data)
    response = next(r for r in response if r["name"] == "Assessment Template")

    expected_errors = [
        errors.MISSING_VALUE_ERROR.format(
            line=5,
            column_name="Default Verifier",
        )
    ]
    expected_warnings = [
        errors.UNKNOWN_USER_WARNING.format(
            line=5,
            column_name="Default Verifier",
            email="user3@a.com",
        ),
        errors.UNKNOWN_USER_WARNING.format(
            line=5,
            column_name="Default Verifier",
            email="user1@a.com"
        ),
    ]
    self.assertEqual(response["rows"], 4)
    self.assertEqual(response["updated"], 0)
    self.assertEqual(response["created"], 3)
    self.assertEqual(response["row_errors"], expected_errors)
    self.assertEqual(response["row_warnings"], expected_warnings)
    self.assertEqual(response["block_errors"], [])
    self.assertEqual(response["block_warnings"], [])
