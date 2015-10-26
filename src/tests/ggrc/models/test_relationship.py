# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: andraz@reciprocitylabs.com
# Maintained By: andraz@reciprocitylabs.com

from ggrc.models.relationship import RelationshipAttr
from tests.ggrc import TestCase


class TestRelationshipAttr(TestCase):

  def test_gather_validators(self):
    class ValidatorParent(object):
      @staticmethod
      def _validate_relationship_attr(cls):
        return True

    class ValidatorChild(ValidatorParent):
      @staticmethod
      def _validate_relationship_attr(cls):
        return False

    validators = RelationshipAttr._gather_validators(ValidatorChild)
    self.assertEqual({True, False}, {v() for v in validators})
