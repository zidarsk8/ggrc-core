# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""Tests relevant to object mapping"""
# pylint: disable=no-self-use
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods
# pylint: disable=unused-argument

import pytest    # pylint: disable=import-error

from lib import base
from lib.utils import conftest_utils


class TestObjectMapping(base.Test):
  """A part of smoke tests, section 4."""

  @pytest.mark.smoke_tests
  def test_mapping_via_lhn(self, selenium, new_program, new_process,
                           new_data_asset, new_system, new_product,
                           new_project):
    """LHN mapping tests from smoke tests, section 6"""
    objects = [new_program, new_process, new_data_asset, new_system,
               new_product, new_project]

    for object_ in objects:
      selenium.driver.get(object_.url)

      for mapped_object in objects:
        # don't map an object to itself
        if mapped_object != object_:
          conftest_utils.get_lhn_accordeon(
              selenium.driver, mapped_object.object_name)\
              .hover_over_visible_member(mapped_object.title_entered.text)\
              .map_to_object()
