# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>


"""Tests for task group task specific export."""
from ggrc import db
from integration.ggrc.models import factories
from integration.ggrc import TestCase


class TestExport(TestCase):
  """Test imports for assessment objects."""

  def setUp(self):
    super(TestExport, self).setUp()
    self.client.get("/login")
    self.headers = {
        'Content-Type': 'application/json',
        "X-Requested-By": "GGRC",
        "X-export-view": "blocks",
    }
    self.comment = factories.CommentFactory(description="123")
    self.assessment = factories.AssessmentFactory()
    self.rel = factories.RelationshipFactory(source=self.comment,
                                             destination=self.assessment)
    extr_comment = factories.CommentFactory(description="bad_desc")
    extr_assessment = factories.AssessmentFactory()
    factories.RelationshipFactory(source=extr_assessment,
                                  destination=extr_comment)

  # pylint: disable=invalid-name
  def assertSlugs(self, field, value, slugs):
    """Assert slugs for selected search"""
    search_request = [{
        "object_name": "Assessment",
        "filters": {
            "expression": {
                "left": field,
                "op": {"name": "="},
                "right": value,
            },
        },
        "fields": ["slug"],
    }]

    parsed_data = self.export_parsed_csv(search_request)["Assessment"]
    self.assertEqual(sorted(slugs),
                     sorted([i["Code*"] for i in parsed_data]))

  def test_search_by_comment(self):
    self.assertSlugs("comment",
                     self.comment.description,
                     [self.assessment.slug])

  def test_search_by_new_comment(self):
    """Filter by added new comment and old comment exists"""
    slugs = [self.assessment.slug]
    desc = "321"
    new_comment = factories.CommentFactory(description=desc)
    factories.RelationshipFactory(source=new_comment,
                                  destination=self.assessment)
    self.assertSlugs("comment", self.comment.description, slugs)
    self.assertSlugs("comment", desc, slugs)

  def test_search_by_deleted_relation(self):
    """Filter by deleted relation to commment"""
    db.session.delete(self.rel)
    db.session.commit()
    self.assertSlugs("comment", self.comment.description, [])

  def test_search_by_deleted_comment(self):
    """Filter by deleted comment"""
    db.session.delete(self.comment)
    db.session.commit()
    self.assertSlugs("comment", self.comment.description, [])
