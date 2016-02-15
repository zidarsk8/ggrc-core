# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com
"""All smoke tests relevant to program page"""

import pytest   # pylint: disable=import-error
from lib import base
from lib import test_helpers
from lib.constants import element
from lib.constants import url
from lib.constants import locator
from lib.page import dashboard
from lib.page import widget_bar
from lib.page import widget


class TestProgramPage(base.Test):
  """A part of smoke tests, section 4."""

  @pytest.mark.smoke_tests
  @staticmethod
  def test_object_count_updates(selenium, new_program):
    """Checks if the count updates in LHN after creating a new program
    object."""
    # pylint: disable=invalid-name
    _, program_info_page = new_program
    lhn_menu = dashboard.DashboardPage(selenium.driver) \
        .open_lhn_menu() \
        .select_my_objects()

    assert lhn_menu.button_programs.members_count \
        >= int(program_info_page.object_id)

  @pytest.mark.smoke_tests
  @staticmethod
  def test_app_redirects_to_new_program_page(new_program):
    """Tests if after saving and closing the lhn_modal the app redirects to
    the object page.

    Generally we start at a random url. Here we verify that after saving
    and closing the lhn_modal we're redirected to an url that contains an
    object id.
    """
    # pylint: disable=invalid-name
    _, program_info_page = new_program
    assert url.PROGRAMS + "/" + program_info_page.object_id in \
        program_info_page.url

  @pytest.mark.smoke_tests
  @staticmethod
  def test_info_tab_is_active_by_default(selenium, new_program):
    """Tests if after the lhn_modal is saved we're redirected and the info
    tab is activated.

    Because the app uses url arguments to remember the state of the page
    (which widget is active), we can simply use the url of the created
    object.
    """
    # pylint: disable=invalid-name
    _, program_info_page = new_program
    program_info_page.navigate_to()
    horizontal_bar = widget_bar.DashboardWidgetBarPage(selenium.driver)

    assert horizontal_bar.get_active_widget_name() == \
        element.LandingPage.PROGRAM_INFO_TAB

  @pytest.mark.smoke_tests
  @staticmethod
  def test_info_tab_contains_entered_data(new_program):
    """Verify that the created object contains the data we've entered
    into the modal."""
    # pylint: disable=invalid-name
    modal, program_info_page = new_program

    assert test_helpers.HtmlParser.parse_text(modal.ui_title.text) == \
        program_info_page.title_entered.text
    assert modal.ui_description.text == \
        program_info_page.description_entered.text
    assert modal.ui_notes.text == program_info_page.notes_entered.text
    assert modal.ui_code.text == program_info_page.code_entered.text
    assert program_info_page.primary_contact_entered.text in \
        modal.ui_primary_contact.text
    assert program_info_page.secondary_contact_entered.text in \
        modal.ui_secondary_contact.text
    assert modal.ui_program_url.text == \
        program_info_page.program_url_entered.text
    assert modal.ui_reference_url.text == \
        program_info_page.reference_url_entered.text
    assert modal.ui_effective_date.text == \
        program_info_page.effective_date_entered.text
    assert modal.ui_stop_date.text == program_info_page.stop_date_entered.text

  @pytest.mark.smoke_tests
  @staticmethod
  def test_permalink(selenium, new_program):
    """Verify the url is copied to clipboard"""
    # pylint: disable=invalid-name
    _, program_info = new_program
    selenium.driver.get(program_info.url)

    program_info_page = widget.ProgramInfo(selenium.driver)
    program_info_page \
        .press_object_settings() \
        .select_get_permalink()

    # test notification alert
    base.AnimatedComponent(
        selenium.driver,
        [locator.Widget.ALERT_LINK_COPIED],
        wait_until_visible=True
    )

    # test generated link
    modal = program_info_page \
        .press_object_settings() \
        .select_edit()
    modal.ui_title.paste_from_clipboard(modal.ui_description)

    assert modal.ui_title.text == program_info_page.url

  @pytest.mark.smoke_tests
  @staticmethod
  def test_edit_modal(selenium, new_program):
    """Tests if data is saved after editing the program info page edit modal"""
    # pylint: disable=invalid-name
    _, program_info = new_program
    selenium.driver.get(program_info.url)

    program_info_page = widget.ProgramInfo(selenium.driver)
    modal = program_info_page \
        .press_object_settings() \
        .select_edit()
    test_helpers.ModalNewProgramPage.enter_test_data(modal)
    test_helpers.ModalNewProgramPage.set_start_end_dates(modal, 1, -2)
    modal.save_and_close()

    updated_program_info_page = widget.ProgramInfo(selenium.driver)
    assert test_helpers.HtmlParser.parse_text(modal.ui_title.text) == \
        updated_program_info_page.title_entered.text
    assert modal.ui_description.text == \
        updated_program_info_page.description_entered.text
    assert modal.ui_notes.text == updated_program_info_page.notes_entered.text
    assert modal.ui_code.text == updated_program_info_page.code_entered.text
    assert updated_program_info_page.primary_contact_entered.text in \
        modal.ui_primary_contact.text
    assert updated_program_info_page.secondary_contact_entered.text in \
        modal.ui_secondary_contact.text
    assert modal.ui_program_url.text == \
        updated_program_info_page.program_url_entered.text
    assert modal.ui_reference_url.text == \
        updated_program_info_page.reference_url_entered.text
    assert modal.ui_effective_date.text == \
        updated_program_info_page.effective_date_entered.text
    assert modal.ui_stop_date.text == \
        updated_program_info_page.stop_date_entered.text
