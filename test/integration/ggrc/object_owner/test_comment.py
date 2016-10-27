# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test object owner of comments."""

from ggrc.models import Request, ObjectOwner, Revision
from integration.ggrc import converters
from integration.ggrc import generator


class TestCommentObjectOwner(converters.TestCase):

  """Test object owner of comments."""

  def setUp(self):
    """Setup test case."""
    converters.TestCase.setUp(self)
    self.response = self.client.get("/login")
    self.generator = generator.ObjectGenerator()

  def test_object_owner(self):
    """Test object owner and its revision of request comment."""

    self.import_file("request_full_no_warnings.csv")
    request1 = Request.query.filter_by(slug="Request 1").first()
    _, comment = self.generator.generate_comment(
        request1, "Verifier", "some comment", send_notification="false")

    object_owner = ObjectOwner.query.filter_by(
        ownable_type='Comment',
        ownable_id=comment.id,
    ).first()
    self.assertIsNotNone(object_owner, "ObjectOwner is not created")

    revision = Revision.query.filter_by(
        resource_type='ObjectOwner',
        resource_id=object_owner.id,
    ).first()
    self.assertIsNotNone(revision, "Revision of ObjectOwner is not created")
