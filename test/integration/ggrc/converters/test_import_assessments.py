# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

# pylint: disable=maybe-no-member

"""Test request import and updates."""

from ggrc import models
from integration.ggrc import converters


class TestRequestImport(converters.TestCase):

  """Basic Request import tests with.

  This test suite should test new Request imports and updates. The main focus
  of these tests is checking error messages for invalid state transitions.
  """

  def setUp(self):
    """ Set up for Request test cases """
    converters.TestCase.setUp(self)
    self.client.get("/login")

  def test_assessments_with_templates(self):
    """Test importing of assessments with templates."""

    self.import_file("assessment_template_no_warnings.csv")
    response = self.import_file("assessment_with_templates.csv")
    self._check_csv_response(response, {})

    assessment = models.Assessment.query.filter(
        models.Assessment.slug == "A 4").first()

    values = set(v.attribute_value for v in assessment.custom_attribute_values)
    self.assertIn("abc", values)
    self.assertIn("2015-07-15 00:00:00", values)
