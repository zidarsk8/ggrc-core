# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com
"""Module for base classes"""

import re

from selenium.webdriver.common import keys    # pylint: disable=import-error
from selenium import webdriver    # pylint: disable=import-error

from lib import constants
from lib import exception
from lib import meta
from lib import mixin
from lib.utils import selenium_utils


class InstanceRepresentation(object):
  def __repr__(self):
    return str(
        {key: value for key, value in self.__dict__.items()
         if "__" not in key})


class CustomDriver(webdriver.Chrome):
  """An extension to the web driver"""

  def find_elements_by_visible_locator(self, locator):
    """
    Sometimes we have to find in a list of elements only that one that is
    visible to the user.
    Args:
        locator (tuple)

    Returns:
        selenium.webdriver.remote.webelement.WebElement

    Raises:
        exception.ElementNotFound
    """
    # pylint: disable=invalid-name
    elements = self.find_elements(*locator)

    for element in elements:
      if element.is_displayed():
        return element

    raise exception.ElementNotFound(locator)


class Test(InstanceRepresentation):
  __metaclass__ = mixin.MetaTestDecorator


class TestUtil(InstanceRepresentation):
  """Abstract class for all test util classes"""


class Element(InstanceRepresentation):
  """The Element class represents primitives in the models"""
  __metaclass__ = meta.RequireDocs

  def __init__(self, driver, locator):
    super(Element, self).__init__()
    self._driver = driver
    self._locator = locator
    self.element = self.get_element()
    self.text = self.element.text

  def get_element(self):
    """
    Returns:
      selenium.webdriver.remote.webelement.WebElement
    """
    return selenium_utils.get_when_visible(self._driver, self._locator)

  def click(self):
    """Clicks on the element"""
    self.element.click()

  def click_when_visible(self):
    """Waits for the element to be visible and only then performs a
    click"""
    selenium_utils.get_when_visible(self._driver, self._locator).click()


class Label(Element):
  """A generic label"""


class RichTextInputField(Element):
  def __init__(self, driver, locator):
    """
    Args:
        driver (CustomDriver):
    """
    super(RichTextInputField, self).__init__(driver, locator)
    self._driver = driver
    self._locator = locator
    self.text = self.element.text

  def enter_text(self, text):
    """Clears the fields and enteres text"""

    self.click_when_visible()
    self.element.clear()
    self.element.send_keys(text)
    self.text = text

  def paste_from_clipboard(self, element):
    """
    Pastes a value from clipboard into text input element.

    Details:
    We want to update the value of this element after pasting. In order to
    do that, we click on another element.

    Args:
      element (Element)
    """
    self.element.clear()
    self.element.send_keys(keys.Keys.CONTROL, 'v')
    element.click()
    element = self._driver.find_element(*self._locator)
    self.text = element.get_attribute("value")


class TextInputField(RichTextInputField):
  """A generic model for the text input field"""


class TextFilterDropdown(Element):
  """Model for elements which are using autocomplete in a text field with a
  dropdown list of found results
  """

  def __init__(self, driver, textbox_locator, dropdown_locator):
    super(TextFilterDropdown, self).__init__(driver, textbox_locator)
    self._locator_dropdown = dropdown_locator
    self._elements_dropdown = None
    self.text_to_filter = None

  def _filter_results(self, text):
    self.text_to_filter = text

    self.element.click()
    self.element.clear()
    self._driver.find_element(*self._locator).send_keys(text)

  def _select_first_result(self):
    # wait that it appears
    selenium_utils.get_when_visible(self._driver, self._locator_dropdown)
    dropdown_elements = self._driver.find_elements(
        *self._locator_dropdown)

    self.text = dropdown_elements[0].text
    dropdown_elements[0].click()
    selenium_utils.get_when_invisible(self._driver, self._locator_dropdown)

  def filter_and_select_first(self, text):
    self._filter_results(text)
    self._select_first_result()


class Iframe(Element):
  """Iframe element methods"""

  def find_iframe_and_enter_data(self, text):
    """
    Args:
        text (basestring): the string we want to enter
    """
    iframe = selenium_utils.get_when_visible(self._driver, self._locator)
    self._driver.switch_to.frame(iframe)

    element = self._driver.find_element_by_tag_name(constants.tag.BODY)
    element.clear()
    element.send_keys(text)

    self._driver.switch_to.default_content()
    self.text = text


class DatePicker(Element):
  """Date picker element methods"""

  def __init__(self, driver, date_picker_locator, field_locator):
    """
    Args:
        date_picker_locator (tuple)
        field_locator (tuple): locator of the field we have to click on to
        activate the date picker
    """
    super(DatePicker, self).__init__(driver, field_locator)
    self._locator_datepcker = date_picker_locator
    self._element_datepicker = None

  def _get_datepicker_elements_for_current_month(self):
    """Gets day elements for current month.

    Returns:
        list of selenium.webdriver.remote.webelement.WebElement
    """
    self.element.click()
    elements = self._driver.find_elements(*self._locator_datepcker)
    return elements

  def select_day_in_current_month(self, day):
    """Selects a day - a sequential element from datepicker. Days go from 0 to
    28,29 or 30, depending on current month. Since we're selecting an element
    from a list, we can pass e.g. -1 to select the last day in month.

    Args:
      day (int)
    """
    elements = self._get_datepicker_elements_for_current_month()
    elements[day].click()

    # wait for fadeout in case we're above some other element
    selenium_utils.get_when_invisible(self._driver, self._locator_datepcker)
    self.text = self.element.get_attribute("value")

  def select_month_end(self):
    """Selects the last day of current month"""
    elements = self._get_datepicker_elements_for_current_month()
    elements[-1].click()

    # wait for fadeout in case we're above some other element
    selenium_utils.get_when_invisible(self._driver, self._locator_datepcker)
    self.text = self.element.get_attribute("value")

  def select_month_start(self):
    """Selects the first day of current month"""
    elements = self._get_datepicker_elements_for_current_month()
    elements[0].click()

    # wait for fadeout in case we're above some other element
    selenium_utils.get_when_invisible(self._driver, self._locator_datepcker)
    self.text = self.element.get_attribute("value")


class Button(Element):
  """A generic button element"""
  def get_element(self):
    return selenium_utils.get_when_clickable(self._driver, self._locator)


class Checkbox(Element):
  """A generic checkboux element"""

  def __init__(self, driver, locator, is_checked=False):
    super(Checkbox, self).__init__(driver, locator)
    self.is_checked = self.element.is_selected()

  def get_element(self):
    return selenium_utils.get_when_clickable(self._driver, self._locator)

  def check(self):
    if not self.is_checked:
      self.element.click()

  def uncheck(self):
    if self.is_checked:
      self.element.click()


class Toggle(Element):
  """A generic toggle element.

  Note that a special function is used for detecting if an element is active
  which may not work on an arbitrary element.
  """

  def __init__(self, driver, locator, is_active_attr_val="active"):
    super(Toggle, self).__init__(driver, locator)
    self.is_activated = selenium_utils.is_value_in_attr(
        self.element, value=is_active_attr_val)

  def get_element(self):
    return selenium_utils.get_when_clickable(self._driver, self._locator)

  def toggle(self, on=True):
    """Clicks on an element based on the is_active status and the "on" arg

    Args:
        on (bool)
    """
    if on and not self.is_activated:
      self.element.click()
      self.is_activated = True
    elif not on and self.is_activated:
      self.element.click()
      self.is_activated = False


class Tab(Element):
  """A generic element representing a tab"""
  def __init__(self, driver, locator, is_activated=True):
    super(Tab, self).__init__(driver, locator)
    self.is_activated = is_activated

  def get_element(self):
    return selenium_utils.get_when_clickable(self._driver, self._locator)

  def click(self):
    """When clicking on a tab we want to first make sure it's clickable i.e.
    that this element will receive a click"""
    selenium_utils.get_when_clickable(self._driver, self._locator).click()
    self.is_activated = True


class Dropdown(Element):
  """A generic dropdown"""


class DropdownStatic(Element):
  """A dropdown with predefined static elements"""

  def __init__(self, driver, dropdown_locator, elements_locator):
    super(DropdownStatic, self).__init__(driver, dropdown_locator)
    self._locator_dropdown_elements = elements_locator
    self.elements_dropdown = self._driver.find_elements(
        *self._locator_dropdown_elements)

  def click(self):
    self.element.click()

  def select(self, member_name):
    """Selects the dropdown element based on dropdown element name"""
    for element in self.elements_dropdown:
      if element.text == member_name:
        element.click()
        break
    else:
      exception.ElementNotFound(member_name)


class Component(InstanceRepresentation):
  """The Component class is a container for elements"""

  __metaclass__ = meta.RequireDocs

  def __init__(self, driver):
    """
    Args:
        driver (CustomDriver)
    """
    self._driver = driver


class AnimatedComponent(Component):
  """Class for components where an animation must first complete before the
  elements are visible"""

  def __init__(self, driver, locators_to_check, wait_until_visible):
    """
    Args:
        driver (CustomDriver)
        locators_to_check (list of tuples): locators to wait for to become
          (in)visible
        wait_until_visible (bool): for all elements to be visible do we
            have to wait for certain elements to be invisible or visible?
    """
    super(AnimatedComponent, self).__init__(driver)
    self._locators = locators_to_check

    if wait_until_visible:
      self._wait_until_visible()
    else:
      self._wait_until_invisible()

  def _wait_until_visible(self):
    for locator in self._locators:
      selenium_utils.get_when_visible(self._driver, locator)

  def _wait_until_invisible(self):
    for locator in self._locators:
      selenium_utils.get_when_invisible(self._driver, locator)


class Modal(Component):
  """A generic modal element"""


class Filter(Component):
  """A gneric filter element"""

  def __init__(self, driver, locator_text_box, locator_submit,
               locator_clear):
    super(Filter, self).__init__(driver)
    self.text_box = TextInputField(driver, locator_text_box)
    self.button_submit = Button(driver, locator_submit)

    # the clear button is only visible after a query is entered
    self.button_clear = driver.find_element(*locator_clear)

  def enter_query(self, query):
    self.text_box.enter_text(query)

  def submit_query(self):
    self.button_submit.click()

  def clear(self):
    """Clears the query field"""
    self.button_clear.click()


class AbstractPage(Component):
  """Represents a page that can be navigate to, but we don't necessarily know
  it's url in advance"""

  def __init__(self, driver):
    super(AbstractPage, self).__init__(driver)
    self.url = driver.current_url

  def navigate_to(self, custom_url=None):
    url_to_use = self.url if custom_url is None else custom_url

    if self._driver.current_url != url_to_use:
      self._driver.get(url_to_use)
    return self


class Page(AbstractPage):
  """The Page class represents components with special properties i.e. they
  have *static* URL-s, can be navigated to etc."""
  URL = None

  def __init__(self, driver):
    """
    Args:
        driver (CustomDriver)
    """
    super(Page, self).__init__(driver)
    self.navigate_to(self.URL)


class DropdownDynamic(AnimatedComponent):
  """A dropdown that doesn't load all the contents at once"""

  def __init__(self, driver, locators_to_check, wait_until_visible):
    """
    Args:
        driver (CustomDriver)
        locators_to_check (list of tuples): locators to wait for to become
          (in)visible
        wait_until_visible (bool): for all elements to be visible do we
            have to wait for certain elements to be invisible or visible?
    """
    super(DropdownDynamic, self).__init__(driver, locators_to_check,
                                          wait_until_visible)
    self.members_visible = None
    self.members_loaded = None

  def _update_loaded_members(self):
    """New members that are loaded are added to the members_loaded
    container"""
    raise NotImplementedError

  def _set_visible_members(self):
    """When moving in the dropdown it can happen we don't always see all
    the members. Here we set the members, that are visible to the user."""
    raise NotImplementedError

  def scroll_down(self):
    raise NotImplementedError

  def scroll_up(self):
    raise NotImplementedError


class Selectable(Element):
  """Representing list of elements that are selectable"""


class Widget(AbstractPage):
  """A page like class for which we don't know the initial url"""

  def __init__(self, driver):
    """
    Args:
        driver (CustomDriver)
    """
    super(Widget, self).__init__(driver)
    object_name, id_, widget_name = re.search(
        constants.regex.URL_WIDGET_INFO, self.url).groups()
    self.object_id = id_
    self.name_from_url = widget_name.split("_")[0] or \
        constants.element.WidgetBar.INFO
    self.object_name = object_name
