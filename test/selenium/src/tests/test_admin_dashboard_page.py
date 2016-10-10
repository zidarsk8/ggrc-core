# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Admin dashboard page smoke tests"""
# pylint: disable=no-self-use
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods

import re
import pytest    # pylint: disable=import-error
from lib import base
from lib import constants
from lib.page import dashboard


class TestAdminDashboardPage(base.Test):
  """Tests for the admin dashboard, a part of smoke tests, section 1"""
  _role_el = constants.element.AdminRolesWidget
  _event_el = constants.element.AdminEventsWidget

  @pytest.fixture(scope="function")
  def admin_dashboard(self, selenium):
    selenium.get(dashboard.AdminDashboard.URL)
    return dashboard.AdminDashboard(selenium)

  @pytest.mark.smoke_tests
  def test_roles_widget(self, admin_dashboard):
    """Check count and content of role scopes"""
    admin_roles_widget = admin_dashboard.select_roles()
    expected_dict = self._role_el.ROLE_SCOPES_DICT
    actual_dict = admin_roles_widget.get_role_scopes_text_as_dict()
    assert admin_dashboard.tab_roles.member_count == len(expected_dict)
    assert expected_dict == actual_dict, "Expected '{}', got '{}'".format(
        expected_dict, actual_dict)

  @pytest.mark.smoke_tests
  def test_events_widget_tree_view_has_data(self, admin_dashboard):
    """Confirms tree view has at least one data row in valid format"""
    admin_events_tab = admin_dashboard.select_events()
    list_of_items = admin_events_tab.get_events()
    assert len(list_of_items) > 0
    items_with_incorrect_format = \
        [getattr(item, 'text') for item in list_of_items if
            not(re.compile(self._event_el.TREE_VIEW_ROW_REGEXP).match(
                getattr(item, 'text')))]
    assert items_with_incorrect_format == []
    assert admin_events_tab.widget_header.text == \
        self._event_el.TREE_VIEW_HEADER
