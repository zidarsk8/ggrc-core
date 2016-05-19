# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: peter@reciprocitylabs.com
# Maintained By: peter@reciprocitylabs.com

"""A module with tests for the GGRC Workflow package.
It contains unit tests for the package's top level utility functions.
"""

import unittest

from mock import MagicMock, patch

from ggrc.models.hooks import assessment


class GetValueTestCase(unittest.TestCase):
  """Tests for the get_value() function."""

  # pylint: disable=invalid-name
  @patch("ggrc.models.hooks.assessment.get_current_user_id")
  @patch("ggrc.models.hooks.assessment.Person")
  def test_returns_auditors_as_default_assessors_when_no_template(
      self, person_class, get_current_user_id
  ):
    """The function should return all Audit's assessors if no template given.
    """
    person_class.query.get.return_value = MagicMock(name="Person XY")
    get_current_user_id.return_value = 42

    person_1 = MagicMock(name="Person Bob")
    person_2 = MagicMock(name="Person John")
    person_3 = MagicMock(name="Person Mike")

    user_role_1 = MagicMock(person=person_1, role=MagicMock())
    user_role_1.role.name = u"Auditor"

    user_role_2 = MagicMock(person=person_2, role=MagicMock())
    user_role_2.role.name = u"Owner"

    user_role_3 = MagicMock(person=person_3, role=MagicMock())
    user_role_3.role.name = u"Auditor"

    audit = MagicMock(name="audit_1")
    audit.context.user_roles = [user_role_1, user_role_2, user_role_3]

    related_object = MagicMock(name="assessment_1")

    people = assessment.get_value(
        "assessors", audit, related_object, template=None)

    self.assertEqual(people, [person_1, person_3])
