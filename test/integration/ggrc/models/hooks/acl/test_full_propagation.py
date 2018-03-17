# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test Full propagation for all objects.

These tests just check that all ACL entries are propagated, but do not check
correct handling on different events (object creation, or deletion). Those
should be covered in a different test suite.

These tests are not full rbac tests and do not take global roles into
consideration.
"""


from integration.ggrc.models import factories
from integration.ggrc import TestCase


class TestFullPropagation(TestCase):
  """TestAuditRoleProgation"""

  CUSTOM_ROLE_OBJECTS = [
      "Program",
      "Audit",
      "Assessment",
      "Control",
      "Issue",
  ]

  def setUp(self):
    super(TestFullPropagation, self).setUp()

    self.people = {}
    self.objects = {}
    with factories.single_commit():
      self.setup_people()
      self.setup_objects()
      self.setup_mappings()

  def setup_custom_roles(self):
    """Create custom roles for propagated acls."""
    for object_type in self.CUSTOM_ROLE_OBJECTS:
      pass

  def setup_people(self):
    """Setup people and global roles"""

  def setup_objects(self):
    """Sets up all the objects needed by the tests"""

  def setup_mappings(self):
    """Sets up all the mappings needed by the tests"""
