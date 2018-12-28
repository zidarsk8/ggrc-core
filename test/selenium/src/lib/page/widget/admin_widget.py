# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Widgets on Admin Dashboard page."""
# pylint: disable=too-few-public-methods

from lib import base, exception
from lib.constants import locator, objects
from lib.constants.element import AdminWidgetEvents
from lib.entities.entities_factory import PeopleFactory
from lib.page import dashboard
from lib.page.widget import widget_base
from lib.utils import date_utils, selenium_utils, string_utils


class Events(dashboard.AdminDashboard):
  """Event widget on Admin Dashboard."""
  _locators = locator.WidgetAdminEvents

  def __init__(self, driver):
    super(Events, self).__init__(driver)
    self.widget_header = base.Label(driver, self._locators.TREE_VIEW_HEADER)

  def _wait_to_be_init(self):
    """Wait when all rows will be visible and ppl emails will be loaded into
    last row.
    """
    selenium_utils.wait_for_js_to_load(self._driver)
    selenium_utils.get_when_all_visible(
        self._driver, self._locators.TREE_VIEW_ITEMS_W_PPL)

  @property
  def events_raw(self):
    """Returns list of strings that displayed in Tree View on Event widget."""
    self._wait_to_be_init()
    events = self._browser.elements(css=self._locators.TREE_VIEW_ITEMS)
    return [event.text for event in events]

  @property
  def events(self):
    """Returns parsed list of dicts for event log records."""
    return [self.parse_event(event_str) for event_str in self.events_raw]

  @staticmethod
  def parse_event(event_str, is_strict=False):
    """Returns parsed event string row based on event regular expression as
    dict of matched groups. If string doesn't match
    regular expression tries to parse 2nd time w/o action in case
    :parameter is_strict = False. Return None for unsuccessful parsing.
    """
    def parse_time(value):
      """Parse string value for "time" to datetime."""
      value["time"] = date_utils.ui_str_with_zone_to_datetime(value["time"])

    parsed_value = string_utils.parse_str_by_reg_exp(
        event_str, AdminWidgetEvents.TREE_VIEW_ROW_REGEXP, True)
    # to workaround migration events and parse them w/o action
    if not parsed_value and is_strict:
      return parsed_value
    if parsed_value:
      parse_time(parsed_value)
      return parsed_value
    parsed_value = string_utils.parse_str_by_reg_exp(
        event_str,
        AdminWidgetEvents.TREE_VIEW_ROW_REGEXP_WO_ACTION, True)
    parse_time(parsed_value)
    return parsed_value

  @property
  def event_datetimes(self):
    """Get list of datetimes for events on the page of Events widget."""
    return [event["time"] for event in self.events]

  @property
  def paging_buttons(self):
    """Get navigation buttons on the tab."""
    self._wait_to_be_init()
    return self._browser.element(id="events_list").elements(
        class_name="view-more-paging")

  def _get_btn_by_name(self, btn_name):
    """Returns buttons by provided name, otherwise None."""
    return next(btn for btn in self.paging_buttons if btn.text == btn_name)

  def _go_to_page(self, btn_name):
    """Find navigation button by name on click if such button exists
    otherwise raise an AttributeError exception.
    """
    self._get_btn_by_name(btn_name).click()
    return self

  def go_to_next_page(self):
    """Go to next page."""
    return self._go_to_page("NEXT PAGE")

  def go_to_prev_page(self):
    """Go to previous page."""
    return self._go_to_page("PREVIOUS PAGE")


class People(dashboard.AdminDashboard):
  """People widget on Admin Dashboard."""
  _locators = locator.WidgetAdminPeople

  def __init__(self, driver):
    super(People, self).__init__(driver)
    self.people_tree_view = base.AdminTreeView(self._driver)

  def get_people(self):
    """Get list of people that displayed in Tree View on People widget.
    """
    tree_view_items = self.people_tree_view.tree_view_items()
    people_as_lists = [item.text.splitlines() for item in tree_view_items]
    return [PeopleFactory().create(
        name=person[0], email=person[1], system_wide_role=person[2])
        for person in people_as_lists]

  def click_create_button(self):
    """Click on the Create button on People widget"""
    add_button = selenium_utils.get_when_clickable(
        self._driver, self._locators.CREATE_PERSON_BUTTON_SELECTOR)
    add_button.click()

  def filter_by_name_email_company(self, str_to_filter_by):
    """Filter people via filter by name email company text field"""
    filter_tf = base.TextInputField(
        self._driver, self._locators.FILTER_BY_NAME_EMAIL_COM_FIELD_SELECTOR)
    filter_tf.enter_text(str_to_filter_by)
    filter_tf.send_enter_key()
    selenium_utils.wait_for_js_to_load(self._driver)


class Roles(dashboard.AdminDashboard):
  """Admin roles widget on Admin Dashboard."""

  def __init__(self, driver):
    super(Roles, self).__init__(driver)
    self.roles_tree_view = base.AdminTreeView(self._driver)

  def get_role_scopes_text_as_dict(self):
    """Get dictionary of labels that displayed in Tree View on Roles widget.
    """
    tree_view_items = self.roles_tree_view.tree_view_items()
    return dict([item.text.splitlines() for item in tree_view_items])


class CustomRoles(dashboard.AdminDashboard):
  """Admin custom roles widget on Admin Dashboard."""

  def __init__(self, driver):
    super(CustomRoles, self).__init__(driver)
    self.custom_roles_tree_view = base.AdminTreeView(self._driver)

  def get_objects_text_as_set(self):
    """Get set of objects labels displayed in Tree View on Custom Roles widget.
    """
    tree_view_items = self.custom_roles_tree_view.tree_view_items()
    return set(item.text for item in tree_view_items)


class CustomAttributes(widget_base.WidgetAdminCustomAttributes):
  """Custom attributes widget on Admin Dashboard page."""

  def __init__(self, driver):
    super(CustomAttributes, self).__init__(driver)
    self.ca_tree_view = base.AdminTreeView(self._driver)

  def expand_collapse_group(self, item_title, expand=True):
    """Expand/collapse 2-nd tier of Tree View item."""
    items = self.get_items_list()
    for i in items:
      if i.text == item_title:
        if expand:
          return i.expand()
        return i.collapse()
    raise exception.ElementNotFound('{} in list {}'.format(item_title, items))

  def get_items_list(self):
    """Return Tree View item objects from current widget."""
    return self.ca_tree_view.tree_view_items()

  def add_custom_attribute(self, ca_obj):
    """Add custom attribute from custom attribute object given."""
    ca_item_content = self.expand_collapse_group(
        objects.get_normal_form(ca_obj.definition_type), expand=True)
    ca_item_content.add_new_custom_attribute(ca_obj)
    self.expand_collapse_group(
        objects.get_normal_form(ca_obj.definition_type), expand=False)

  def get_custom_attributes_list(self, ca_group):
    """Collect custom attributes from expanded custom attribute group
    Tree View.
    """
    ca_item_content = self.expand_collapse_group(
        objects.get_normal_form(ca_group.definition_type), expand=True)
    return ca_item_content.get_ca_list_from_group()


class ModalCustomAttributes(widget_base.CustomAttributeModal):
  """Custom attributes modal."""
