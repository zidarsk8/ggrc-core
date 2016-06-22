# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from ggrc import db
from ggrc.models import Assessment
from integration.ggrc import TestCase
from integration.ggrc.models.factories import AssessmentFactory


class TestAssessment(TestCase):

  def test_auto_slug_generation(self):
    AssessmentFactory(title="Some title")
    db.session.commit()
    ca = Assessment.query.first()
    self.assertEqual("ASSESSMENT-{}".format(ca.id), ca.slug)
