# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""
Utility classes for page objects used in tests.

Details:
Most of the tests require a sequence of primitive methods of the page
object. If the sequence repeats itself among tests, it should be shared in
this module.
"""

import uuid
import re
from lib import base
from lib.constants.test import modal_create_new
from lib.constants.test import modal_custom_attribute


def add_random_string_after(text):
  return text + str(uuid.uuid4())


def add_random_string_before(text):
  return str(uuid.uuid4()) + text


class HtmlParser(base.Test):
  """The HtmlParser class simulates what happens with (non-rich)text in HTML.
  """
  @staticmethod
  def parse_text(text):
    """Simulates text parsed by html

    Args:
      text (str or unicode)
    """
    return re.sub(r'\s+', " ", text)


class ModalNewControlPage(base.Test):
  """Methods for simulating common user actions"""

  @staticmethod
  def enter_test_data(modal):
    """Fills out all fields in the lhn_modal

    Args:
        modal (lib.page.lhn_modal.new_control.NewControlModal)
    """
    modal.enter_title(add_random_string_after(modal_create_new.SHORT_TITLE))
    modal.enter_description(add_random_string_after(modal_create_new.SHORT_TITLE))
    modal.enter_test_plan(add_random_string_after(modal_create_new.SHORT_TITLE))
    modal.enter_notes(add_random_string_after(modal_create_new.SHORT_TITLE))
    modal.enter_code(add_random_string_after(modal_create_new.SHORT_TITLE))


class ModalNewProgramPage(base.Test):
  """Methods for simulating common user actions"""

  @staticmethod
  def enter_test_data(modal):
    """Fills out all fields in the lhn_modal

    Args:
        modal (lib.page.modal.edit_object.EditProgramModal)
    """
    modal.enter_title(add_random_string_after(modal_create_new.SHORT_TITLE))
    modal.enter_description(add_random_string_after(
        modal_create_new.SHORT_TITLE))
    modal.enter_notes(add_random_string_after(modal_create_new.SHORT_TITLE))
    modal.enter_code(add_random_string_after(modal_create_new.SHORT_TITLE))
    modal.filter_and_select_primary_contact("example")
    modal.filter_and_select_secondary_contact("example")
    modal.enter_program_url(add_random_string_before(
        modal_create_new.Program.PROGRAM_URL))
    modal.enter_reference_url(add_random_string_before(
        modal_create_new.Program.REFERENCE_URL))

  @staticmethod
  def set_start_end_dates(modal, day_start, day_end):
    """
    Sets the dates from the datepicker in the new program/edit modal.

    Args:
      modal (lib.page.modal.edit_object.EditProgramModal)
      day_start (int): for more info see
        base.DatePicker.select_day_in_current_month
      day_end (int): for more info see
        base.DatePicker.select_day_in_current_month
    """
    modal.enter_effective_date_start_month(day_start)
    modal.enter_stop_date_end_month(day_end)


class ModalNewProgramCustomAttributePage(base.Test):
  @staticmethod
  def enter_test_data(modal):
    """Fills out all fields in the lhn_modal

    Args:
        modal (lib.page.modal.custom_attribute.NewCustomAttributeModal)
    """
    modal.enter_title(add_random_string_after(
        modal_custom_attribute.Program.TITLE))
    modal.enter_inline_help(add_random_string_after(
        modal_custom_attribute.Program.INLINE_HELP))
    modal.enter_placeholder(add_random_string_after(
        modal_custom_attribute.Program.PLACEHOLDER))


class ModalNewOrgGroupPage(base.Test):
  @staticmethod
  def enter_test_data(modal):
    """Fills out all fields in the lhn_modal

    Args:
        modal (lib.page.modal.edit_object.EditOrgGroupModal)
    """
    modal.enter_title(add_random_string_after(
      modal_custom_attribute.Program.TITLE))


class ModalRiskPage(base.Test):
  @staticmethod
  def enter_test_data(modal):
    """Fills out all fields in the lhn_modal

    Args:
        modal (lib.page.modal.edit_object.EditRiskModal)
    """
    modal.enter_title(add_random_string_after(
      modal_custom_attribute.Program.TITLE))
    modal.enter_description(add_random_string_after(
      modal_custom_attribute.Program.TITLE))

