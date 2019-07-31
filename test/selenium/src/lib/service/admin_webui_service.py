# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Services for create and manipulate objects via admin UI."""

from nerodia.wait import wait

from lib import url
from lib.page import dashboard
from lib.page.modal import person_modal
from lib.utils import selenium_utils


class AdminWebUiService(object):
  """Base class for business layer's services objects for Admin."""

  # pylint: disable=too-few-public-methods
  def __init__(self, driver):
    self._driver = driver


class PeopleAdminWebUiService(AdminWebUiService):
  """Class for admin people business layer's services objects"""

  def __init__(self, driver=None):
    super(PeopleAdminWebUiService, self).__init__(driver)
    self.people_widget = self._open_admin_people_tab()

  def create_new_person(self, person):
    """Create new person on Admin People widget
      - Return: lib.entities.entity.PersonEntity"""
    self.people_widget.click_create_button()
    self._fill_and_submit_modal_form(person)
    # refresh page to make newly created person appear on Admin People Widget
    self._driver.refresh()
    return self.find_filtered_person(person)

  def _open_admin_people_tab(self):
    """Open People widget on Admin dashboard.
      - Return: lib.page.widget.admin_widget.People"""
    selenium_utils.open_url(url.Urls().admin_people_tab)
    return dashboard.AdminDashboard(self._driver).select_people()

  def _fill_and_submit_modal_form(self, person):
    """Get data from person object, fill and submit the form."""
    modal = person_modal.BasePersonModal(self._driver)
    data = {"name": person.name, "email": person.email}
    if person.company:
      data["company"] = person.company
    modal.fill_and_submit_form(**data)
    selenium_utils.wait_for_js_to_load(self._driver)

  def find_filtered_person(self, person):
    """Find person by email in the list on Admin People widget
      - Return: list of PersonEntities"""
    self.people_widget.filter_by_name_email_company(person.email)
    selenium_utils.wait_for_js_to_load(self._driver)
    return self.people_widget.get_people()[0]

  @property
  def ppl_count(self):
    """Get ppl count from tab."""
    return self.people_widget.tab_people.count

  def expand_found_person(self, person):
    """Find and expand person from people tree item."""
    self.find_filtered_person(person)
    return self.people_widget.expand_top_person()

  def edit_person(self, person_to_edit, new_person):
    """Open Edit Modal window for person_to_edit and submit form filled with
    new_person data."""
    self.expand_found_person(person_to_edit).open_edit_modal()
    self._fill_and_submit_modal_form(new_person)

  def edit_authorizations(self, person, new_role):
    """Open User Role Assignments Modal window for selected person and apply
    new role.
    Return edited person."""
    people_tree_item = self.expand_found_person(person)
    people_tree_item.open_edit_authorizations_modal().select_and_submit_role(
        new_role)
    wait.Wait.until(
        lambda: people_tree_item.get_person().system_wide_role == new_role)
    return self.expand_found_person(person).get_person()
