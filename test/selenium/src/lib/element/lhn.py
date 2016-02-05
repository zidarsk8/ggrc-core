# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

from lib import base
from lib.constants import locator


class _Tab(base.Tab):
    locator_element = None

    def __init__(self, driver):
        """
        Args:
            driver (base.CustomDriver
        """
        super(_Tab, self).__init__(driver, self.locator_element)


class MyObjectsTab(_Tab):
    locator_element = locator.LhnMenu.MY_OBJECTS


class AllObjectsTab(_Tab):
    locator_element = locator.LhnMenu.ALL_OBJECTS


class Button(base.Button):
    def __init__(self, driver, locator_element, locator_count):
        super(Button, self).__init__(driver, locator_element)
        self.members_count = int(
            self._driver.find_element(*locator_count).text)


class DropdownStatic(base.Dropdown):
    _locator_element = None

    def __init__(self, driver):
        super(DropdownStatic, self).__init__(driver, self._locator_element)


class AccordionGroup(base.DropdownDynamic):
    """Class which models LHN top level buttons/elements."""

    _locator_spinny = None
    _locator_button_create_new = None

    def __init__(self, driver):
        """
        Args:
            driver (base.CustomDriver)
        """
        super(AccordionGroup, self).__init__(
            driver,
            [self._locator_spinny],
            wait_until_visible=False
        )

        self.button_create_new = base.Button(
            self._driver, self._locator_button_create_new)

        # todo
        # self._update_loaded_members()
        # self._set_visible_members()

    def _update_loaded_members(self):
        pass

    def _set_visible_members(self):
        pass

    def scroll_down(self):
        pass

    def scroll_up(self):
        pass

    def create_new(self):
        pass
