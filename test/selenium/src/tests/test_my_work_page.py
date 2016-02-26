# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""All smoke tests relevant to my work page"""
# pylint: disable=no-self-use
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods
# pylint: disable=unused-argument

import pytest    # pylint: disable=import-error

from lib import base
from lib import exception
from lib.page import dashboard
from lib.constants.test import batch
from lib.page.widget import controls
from lib import conftest_utils


class TestMyWorkPage(base.Test):
  """Tests the my work page, a part of smoke tests, section 2"""

  @pytest.mark.smoke_tests
  def test_horizontal_nav_bar_tabs(self, selenium, battery_of_controls):
    """Tests that several objects in a widget can be deleted sequentially"""
    controls_widget = dashboard\
        .DashboardPage(selenium.driver)\
        .select_controls()

    try:
      for _ in xrange(batch.BATTERY):
        controls_widget\
            .select_nth_member(0)\
            .press_object_settings()\
            .select_edit()\
            .delete_object()\
            .confirm_delete()
    except exception.RedirectTimeout:
      # we expect this exception since the url will stay the same for the last
      # deleted member in object list in a widget
      assert controls.Controls(selenium.driver).members_listed == []
    else:
      assert False

  @pytest.mark.smoke_tests
  def test_redirect(self, selenium):
    """Tests if the user is redirected to the My Work page after clicking on
    the my work button in user dropdown"""
    conftest_utils.navigate_to_page_that_contains_lhn(selenium.driver)

    dashboard.HeaderPage(selenium.driver)\
        .open_user_list()\
        .select_my_work()

    assert selenium.driver.current_url == dashboard.DashboardPage.URL
