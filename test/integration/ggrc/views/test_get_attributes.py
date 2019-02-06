# -*- coding: utf-8 -*-
# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Integration tests for get all attributes json"""

import json
import ddt

from ggrc.views import get_all_attributes_json

from integration.ggrc.services import TestCase
from integration.ggrc.models import factories


@ddt.ddt
class TestGetAttributes(TestCase):
  """Test get all attributes json"""

  def setUp(self):
    super(TestGetAttributes, self).setUp()
    self.clear_data()
    self.client.get("/login")

  @ddt.data(
      (u"Война", "Risk"),
      (u"戰爭", "Program"),
      (u"Krieg".encode("ascii"), "Audit"),
  )
  @ddt.unpack
  def test_get_attributes(self, role_name, object_type):
    """Test get all attributes json"""
    factories.AccessControlRoleFactory(
        name=role_name,
        object_type=object_type
    )
    all_attrs_str = get_all_attributes_json(load_custom_attributes=True)
    all_attrs = json.loads(all_attrs_str)
    all_attrs_for_type = all_attrs[object_type]
    self.assertIn(role_name, (x["attr_name"] for x in all_attrs_for_type))
