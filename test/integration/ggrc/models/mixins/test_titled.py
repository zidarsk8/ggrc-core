# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Integration test for Titled mixin"""

import ddt

from ggrc.models import all_models

from integration.ggrc import TestCase
from integration.ggrc.api_helper import Api


@ddt.ddt
class TestTitledMixin(TestCase):
  """Test cases for Labeled mixin"""

  def setUp(self):
    super(TestTitledMixin, self).setUp()
    self.api = Api()
    self.api.login_as_normal()

  def test_post_no_title(self):
    """Test object creation request without title key"""
    response = self.api.post(all_models.Product,
                             {'product': {"description": "desc"}})

    self.assert400(response)
    self.assertEqual(response.json, "'title' must be specified")

  def test_post_title_is_none(self):
    """Test object creation request title=None"""
    response = self.api.post(
        all_models.Product,
        {'product': {"description": "desc", "title": None}}
    )

    self.assert400(response)
    self.assertEqual(response.json, "'title' must be specified")

  def test_post_title_is_empty(self):
    """Test object creation request title=\"\""""
    response = self.api.post(
        all_models.Product,
        {'product': {"description": "desc", "title": ""}}
    )

    self.assertStatus(response, 201)
