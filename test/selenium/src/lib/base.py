# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com
"""Module for base classes"""

import time
import pyvirtualdisplay   # pylint: disable=import-error

# pylint: disable=import-error
from selenium.webdriver.support import expected_conditions as EC

# pylint: disable=import-error
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common import keys    # pylint: disable=import-error
from selenium import webdriver    # pylint: disable=import-error
from lib import environment
from lib import constants
from lib import exception
from lib import meta
from lib import mixin


class InstanceRepresentation(object):
  def __repr__(self):
    return str(
        {key: value for key, value in self.__dict__.items()
         if "__" not in key}
    )


class CustomDriver(webdriver.Chrome):
  def __init__(self, **kwargs):
    super(CustomDriver, self).__init__(**kwargs)

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


class Selenium(object):
  __metaclass__ = mixin.MetaDocsDecorator

  def __init__(self):
    """Prepares resources.

    Configures virtual display buffer for running the test suite in
    headless mode. Also the webdriver is configured here with custom
    resolution and separate log path.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--verbose")

    self.display = pyvirtualdisplay.Display(
        visible=environment.DISPLAY_WINDOWS,
        size=environment.WINDOW_RESOLUTION
    )
    self.display.start()
    self.driver = CustomDriver(
        executable_path=environment.CHROME_DRIVER_PATH,
        chrome_options=options,
        service_log_path=environment.PROJECT_ROOT_PATH +
        constants.path.LOGS_DIR +
        constants.path.CHROME_DRIVER
    )
    width, height = environment.WINDOW_RESOLUTION
    self.driver.set_window_size(width, height)

  def close_resources(self):
    """Closes resources.

    Closes and quits used resources in testing methods to prevent leaks and
    saves a screenshot on error with a unique file name.
    """
    self.driver.quit()
    self.display.stop()


class Test(InstanceRepresentation):
  __metaclass__ = mixin.MetaDocsDecorator


class Element(InstanceRepresentation):
  """The Element class represents primitives in the models"""
  __metaclass__ = meta.RequireDocs

  def __init__(self, driver, locator):
    """
    Args:
        driver (CustomDriver):
    """
    super(Element, self).__init__()
    self._driver = driver
    self._locator = locator
    self._element = driver.find_element(*locator)
    self.text = self._element.text

  def click(self):
    """Clicks on the element"""
    self._element.click()

  def get_when_invisible(self, locator=None):
    """
    Some elements, upon activation, are overlaying others. Here we wait
    for the animation to end so that we can interact with the elements
    below the overlay.

    Returns:
        selenium.webdriver.remote.webelement.WebElement
    """
    locator_to_use = locator if locator else self._locator

    element = WebDriverWait(
        self._driver,
        constants.ux.MAX_USER_WAIT_SECONDS) \
        .until(EC.invisibility_of_element_located(locator_to_use))
    return element

  def get_when_visible(self, locator=None):
    """
    Returns:
        selenium.webdriver.remote.webelement.WebElement
    """
    locator_to_use = locator if locator else self._locator

    element = WebDriverWait(
        self._driver,
        constants.ux.MAX_USER_WAIT_SECONDS) \
        .until(EC.element_to_be_clickable(locator_to_use))

    return element

  def click_when_visible(self, locator=None):
    """Waits for the element to be visible and only then performs a
    click"""
    self.get_when_visible(locator).click()

  def click_when_moving_over(self):
    """Waits until the element stops moving"""

    prev_location = None
    timer_begin = time.time()

    while prev_location != self._element.location:
      prev_location = self._element.location
      time.sleep(0.1)

      if time.time() - timer_begin > constants.ux.ELEMENT_MOVING_TIMEOUT:
        raise exception.ElementMovingTimeout(self._locator)

    self._element.click()


class Label(Element):
  pass


class RichTextInputField(Element):
  def __init__(self, driver, locator):
    """
    Args:
        driver (CustomDriver):
    """
    self._driver = driver
    self._locator = locator
    self._element = self.get_when_visible(locator)
    self.text = self._element.text

  def enter_text(self, text):
    self.click_when_visible()
    self._element.clear()
    self._element.send_keys(text)
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
    self._element.clear()
    self._element.send_keys(keys.Keys.CONTROL, 'v')
    element.click()
    el = self._driver.find_element(
        *self._locator)
    self.text = el.get_attribute("value")


class TextInputField(RichTextInputField):
  def enter_text(self, text):
    super(TextInputField, self).enter_text(text)


class TextFilterDropdown(Element):
  def __init__(self, driver, textbox_locator, dropdown_locator):
    super(TextFilterDropdown, self).__init__(driver, textbox_locator)
    self._locator_dropdown = dropdown_locator
    self._elements_dropdown = None
    self.text_to_filter = None

  def _filter_results(self, text):
    self.text_to_filter = text

    self._element.click()
    self._element.clear()
    self._driver.find_element(*self._locator).send_keys(text)

  def _select_first_result(self):
    # wait that it appears
    self.get_when_visible(self._locator_dropdown)
    dropdown_elements = self._driver.find_elements(
        *self._locator_dropdown)

    self.text = dropdown_elements[0].text
    dropdown_elements[0].click()
    self.get_when_invisible(self._locator_dropdown)

  def filter_and_select_first(self, text):
    self._filter_results(text)
    self._select_first_result()


class Iframe(Element):
  def find_iframe_and_enter_data(self, text):
    """
    Args:
        text (str): the string we want to enter
    """
    iframe = self.get_when_visible()
    self._driver.switch_to.frame(iframe)

    element = self._driver.find_element_by_tag_name(constants.tag.BODY)
    element.clear()
    element.send_keys(text)

    self._driver.switch_to.default_content()
    self.text = text


class DatePicker(Element):
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
    self._element.click()
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
    self.get_when_invisible(self._locator_datepcker)
    self.text = self._element.get_attribute("value")

  def select_month_end(self):
    """Selects the last day of current month"""
    elements = self._get_datepicker_elements_for_current_month()
    elements[-1].click()

    # wait for fadeout in case we're above some other element
    self.get_when_invisible(self._locator_datepcker)
    self.text = self._element.get_attribute("value")

  def select_month_start(self):
    """Selects the first day of current month"""
    elements = self._get_datepicker_elements_for_current_month()
    elements[0].click()

    # wait for fadeout in case we're above some other element
    self.get_when_invisible(self._locator_datepcker)
    self.text = self._element.get_attribute("value")


class Button(Element):
  pass


class Checkbox(Element):
  def __init__(self, driver, locator, is_checked=False):
    super(Checkbox, self).__init__(driver, locator)
    self.is_checked = is_checked

  def click(self):
    self._element.click()
    self.is_checked = not self.is_checked


class Toggle(Element):
  def __init__(self, driver, locator, is_activated=False):
    super(Toggle, self).__init__(driver, locator)
    self.is_activated = is_activated

  def click(self):
    self._element.click()
    self.is_activated = not self.is_activated


class Tab(Element):
  def __init__(self, driver, locator, is_activated=True):
    super(Tab, self).__init__(driver, locator)
    self.is_activated = is_activated

  def click(self):
    self._element.click()
    self.is_activated = True


class Dropdown(Element):
  def select(self, option_locator):
    """Select an option from a dropdown menu

    Args:
        option_locator (tuple): locator of the dropdown element
    """
    self._element.click()
    self._driver.find_element(*option_locator).click()


class DropdownStatic(Element):
  """A dropdown with predefined static elements"""

  def __init__(self, driver, dropdown_locator, elements_locator):
    super(DropdownStatic, self).__init__(driver, dropdown_locator)
    self._locator_dropdown_elements = elements_locator
    self.elements_dropdown = self._driver.find_elements(
        *self._locator_dropdown_elements)

  def click(self):
    self._element.click()

  def select(self, member_name):
    """Selects the dropdown element based on dropdown element name"""
    for element in self.elements_dropdown:
      if element.text == member_name:
        element.click()
        break
    else:
      exception.ElementNotFound(member_name)


class Component(object):
  """The Component class is a container for elements"""
  __metaclass__ = meta.RequireDocs

  def __init__(self, driver):
    """
    Args:
        driver (CustomDriver)
    """
    self._driver = driver

  def wait_for_redirect(self):
    """Wait until the current url changes"""
    from_url = self._driver.current_url

    while from_url == self._driver.current_url:
      time.sleep(0.1)


class AnimatedComponent(Component):
  """Class for components where an animation must first complete before the
  elements are visible"""

  def __init__(self, driver, locators_to_check, wait_until_visible):
    """
    Args:
        driver (CustomDriver)
        locators_to_check (list of tuples): list of locators
        wait_until_visible (bool): for all elements to be visible do we
            have to wait for certain elements to be invisible or visible?
    """
    super(AnimatedComponent, self).__init__(driver)
    self._locators = locators_to_check

    self._wait_until_visible() if wait_until_visible \
        else self._wait_until_invisible()

  def _wait_until_visible(self):
    for locator in self._locators:
      WebDriverWait(self._driver, constants.ux.MAX_USER_WAIT_SECONDS) \
          .until(EC.element_to_be_clickable(locator))

  def _wait_until_invisible(self):
    for locator in self._locators:
        WebDriverWait(self._driver, constants.ux.MAX_USER_WAIT_SECONDS) \
            .until(EC.invisibility_of_element_located(locator))


class Modal(Component):
  pass


class Filter(Component):
  def __init__(self, driver, locator_text_box, locator_submit,
               locator_clear):
    super(Filter, self).__init__(driver)
    self.text_box = TextInputField(driver, locator_text_box)
    self.button_submit = Button(driver, locator_submit)
    self.button_clear = Button(driver, locator_clear)

  def enter_query(self, query):
    self.text_box.enter_text(query)

  def submit_query(self):
    self.button_submit.click()

  def clear(self):
    self.button_clear.click()


class AbstractPage(Component):
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
  have URL-s, can be navigated to etc."""
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
        locators_to_check (list of tuples): list of locators
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


class Widget(AbstractPage):
  """A page like class for which we don't know the initial url"""

  def __init__(self, driver):
    """
    Args:
        driver (CustomDriver)
    """
    super(Widget, self).__init__(driver)
