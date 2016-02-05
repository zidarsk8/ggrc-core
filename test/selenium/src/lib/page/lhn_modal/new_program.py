# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

from lib import base
from lib.page.widget import info
from lib.constants import locator


class NewProgramModal(base.Modal):
    _locators = locator.ModalCreateNewProgram

    def __init__(self, driver):
        super(NewProgramModal, self).__init__(driver)
        # user input elements
        self.ui_title = base.TextInputField(self._driver,
                                            self._locators.UI_TITLE)
        self.ui_description = base.Iframe(
            self._driver, self._locators.UI_DESCRIPTION)
        self.ui_notes = base.Iframe(self._driver,
                                    self._locators.NOTES_UI)
        self.ui_code = base.TextInputField(self._driver,
                                           self._locators.UI_CODE)
        self.ui_state = base.Dropdown(self._driver, self._locators.UI_STATE)
        self.ui_show_optional_fields = base.Toggle(
            self._driver,
            self._locators.BUTTON_SHOW_ALL_OPTIONAL_FIELDS)
        self.ui_primary_contact = base.TextFilterDropdown(
            self._driver,
            self._locators.UI_PRIMARY_CONTACT,
            self._locators.DROPDOWN_CONTACT)
        self.ui_secondary_contact = base.TextFilterDropdown(
            self._driver,
            self._locators.UI_SECONDARY_CONTACT,
            self._locators.DROPDOWN_CONTACT)
        self.ui_program_url = base.TextInputField(
            self._driver, self._locators.UI_PROGRAM_URL)
        self.ui_reference_url = base.TextInputField(
            self._driver, self._locators.UI_REFERENCE_URL)
        self.ui_effective_date = base.DatePicker(
            self._driver,
            self._locators.DATE_PICKER,
            self._locators.UI_EFFECTIVE_DATE)
        self.ui_stop_date = base.DatePicker(
            self._driver,
            self._locators.DATE_PICKER,
            self._locators.UI_STOP_DATE)

        # static elements
        self.title = base.Label(self._driver, self._locators.TITLE)
        self.description = base.Label(self._driver, self._locators.DESCRIPTION)
        self.program_url = base.Label(self._driver, self._locators.PROGRAM_URL)
        self.button_save_and_add_another = base.Button(
            self._driver,
            self._locators.BUTTON_SAVE_AND_ADD_ANOTHER)
        self.button_save_and_close = base.Button(
            self._driver,
            self._locators.BUTTON_SAVE_AND_CLOSE)

    def enter_title(self, text):
        """Enters the text into the title base.

        Args:
            text (str or unicode)
        """
        self.ui_title.enter_text(text)

    def enter_description(self, description):
        """Enters the text into the description element

        Args:
            description (str)
        """
        self.ui_description.find_iframe_and_enter_data(description)

    def enter_notes(self, notes):
        """Enters the text into the notes element

        Args:
            notes (str)
        """
        self.ui_notes.find_iframe_and_enter_data(notes)

    def enter_code(self, code):
        """Enters the text into the code element

        Args:
            code (str or unicode)
        """
        self.ui_code.enter_text(code)

    def select_state(self, state):
        """Selects a state from the dropdown"""
        raise NotImplementedError

    def toggle_optional_fields(self):
        """Shows or hides optional fields"""
        raise NotImplementedError

    def filter_and_select_primary_contact(self, text):
        """Enters the text into the primary contact element"""
        self.ui_primary_contact.filter_and_select_first(text)

    def filter_and_select_secondary_contact(self, text):
        """Enters the text into the secondary contact element"""
        self.ui_secondary_contact.filter_and_select_first(text)

    def enter_program_url(self, url):
        """Enters the program url for this program object

        Args:
            url (str)
        """
        self.ui_program_url.enter_text(url)

    def enter_reference_url(self, url):
        """Enters the reference url for this program object

        Args:
            url (str)
        """
        self.ui_reference_url.enter_text(url)

    def enter_effective_date_start_month(self):
        """Selects from datepicker the start date"""
        self.ui_effective_date.select_month_start()

    def enter_stop_date_end_month(self):
        """Selects from datepicker the end date"""
        self.ui_stop_date.select_month_end()

    def save_and_add_other(self):
        """Saves this objects and opens a new form"""
        self.button_save_and_add_another.click()
        return NewProgramModal(self._driver)

    def save_and_close(self):
        """Saves this object.

        Note that at least the title must be entered and it must be unique.
        """
        self.button_save_and_close.click()
        self.wait_for_redirect()
        return info.ProgramInfo(self._driver)
