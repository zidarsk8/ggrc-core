# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>


"""Tests for task group task specific export."""
from ddt import data, ddt

from ggrc import db
from integration.ggrc.models import factories
from integration.ggrc import TestCase


@ddt
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
    extr_comment = factories.CommentFactory(description="bad_desc")
    extr_assessment = factories.AssessmentFactory()
    db.engine.execute(
        'update assessments set '
        'updated_at = "2010-10-10", '
        'created_at = "2010-10-10";'
    )
    factories.RelationshipFactory(source=extr_assessment,
                                  destination=extr_comment)
    self.comment = factories.CommentFactory(description="123")
    self.assessment = factories.AssessmentFactory()
    self.rel = factories.RelationshipFactory(source=self.comment,
                                             destination=self.assessment)

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

  def filter_by_datetime(self, alias, value, slugs):
    """Util function, check date for all valid formats"""
    parts = ["year", "month", "day", "hour", "minute", "second"]
    kwargs = {i: getattr(value, i) for i in parts}
    formats = [
        "{year}",
        "{year}-{month}",
        "{year}-{month}-{day}",
        "{year}-{month}-{day}:{hour}",
        "{year}-{month}-{day}:{hour}:{minute}",
        "{year}-{month}-{day}:{hour}:{minute}:{second}",
    ]
    for f_str in formats:
      self.assertSlugs(alias, f_str.format(**kwargs), slugs)

  @data("created_at", "Created On", "created on")
  def test_filter_by_created_at(self, alias):
    """Test filter by created at"""
    self.filter_by_datetime(alias,
                            self.assessment.created_at,
                            [self.assessment.slug])

  @data("updated_at", "Last Updated", "Last Updated")
  def test_filter_by_updated_at(self, alias):
    """Test filter by updated at"""
    self.filter_by_datetime(alias,
                            self.assessment.updated_at,
                            [self.assessment.slug])
