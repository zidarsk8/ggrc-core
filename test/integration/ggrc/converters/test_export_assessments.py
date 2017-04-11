# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>


"""Tests for task group task specific export."""
import datetime
from ddt import data, ddt

from ggrc import db
from ggrc.models import all_models
from integration.ggrc.models import factories
from integration.ggrc import TestCase


@ddt
class TestExport(TestCase):
  """Test imports for assessment objects."""

  model = all_models.Assessment

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
    self.assessment = factories.AssessmentFactory(
        verified_date=datetime.datetime.now(),
        finished_date=datetime.datetime.now(),
    )
    self.rel = factories.RelationshipFactory(source=self.comment,
                                             destination=self.assessment)

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

  @data("created_at", "Created On", "created on")
  def test_filter_by_created_at(self, alias):
    """Test filter by created at"""
    self.assertFilterByDatetime(alias,
                                self.assessment.created_at,
                                [self.assessment.slug])

  @data("updated_at", "Last Updated", "Last Updated")
  def test_filter_by_updated_at(self, alias):
    """Test filter by updated at"""
    self.assertFilterByDatetime(alias,
                                self.assessment.updated_at,
                                [self.assessment.slug])

  @data("finished_date", "Finished Date", "finished date")
  def test_filter_by_finished_date(self, alias):
    """Test filter by finished date"""
    self.assertFilterByDatetime(alias,
                                self.assessment.finished_date,
                                [self.assessment.slug])

  @data("verified_date", "Verified Date", "verified date")
  def test_filter_by_verified_date(self, alias):
    """Test filter by verified date"""
    self.assertFilterByDatetime(alias,
                                self.assessment.verified_date,
                                [self.assessment.slug])
