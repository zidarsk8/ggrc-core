# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from ggrc.models import Assessment
from integration.ggrc import TestCase
from integration.ggrc.models.factories import AssessmentFactory


class TestAssessment(TestCase):
  # pylint: disable=invalid-name

  def test_auto_slug_generation(self):
    AssessmentFactory(title="Some title")
    ca = Assessment.query.first()
    self.assertEqual("ASSESSMENT-{}".format(ca.id), ca.slug)

  def test_enabling_comment_notifications_by_default(self):
    """New Assessments should have comment notifications enabled by default."""
    AssessmentFactory()
    asmt = Assessment.query.first()

    self.assertTrue(asmt.send_by_default)
    recipients = asmt.recipients.split(",") if asmt.recipients else []
    self.assertEqual(sorted(recipients), ["Assessor", "Creator", "Verifier"])
