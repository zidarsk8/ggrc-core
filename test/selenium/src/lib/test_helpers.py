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
from lib import base
from lib.constants.test import modal_create_new
from lib.constants.test import modal_custom_attribute


class HtmlParser(base.Test):
  @staticmethod
  def parse_text(text):
    """Simulates text parsed by html
    Args:
      text (str)
    """
    return text.replace("  ", "").replace("\n", "")


class ModalNewProgramPage(base.Test):
  """Methods for simulating common user actions"""

  @staticmethod
  def enter_test_data(modal):
    """Fills out all fields in the lhn_modal

    Args:
        modal (lib.page.lhn_modal.new_program.EditProgramModal)
    """
    unique_id = str(uuid.uuid4())

    modal.enter_title(modal_create_new.Program.TITLE + unique_id)
    modal.enter_description(
        modal_create_new.Program.DESCRIPTION_SHORT + unique_id)
    modal.enter_notes(
        modal_create_new.Program.NOTES_SHORT + unique_id)
    modal.enter_code(modal_create_new.Program.CODE + unique_id)
    modal.filter_and_select_primary_contact("example")
    modal.filter_and_select_secondary_contact("example")
    modal.enter_program_url(
        unique_id + modal_create_new.Program.PROGRAM_URL)
    modal.enter_reference_url(
        unique_id + modal_create_new.Program.REFERENCE_URL)

  @staticmethod
  def set_start_end_dates(modal, day_start, day_end):
    """
    Sets the dates from the datepicker in the new program/edit modal.

    Args:
      modal (lib.page.lhn_modal.new_program.EditProgramModal)
      day_start (int): for more info see
        base.DatePicker.select_day_in_current_month
      day_end (int): for more info see
        base.DatePicker.select_day_in_current_month
    """
    modal.enter_effective_date_start_month(day_start)
    modal.enter_stop_date_end_month(day_end)


class ModalNewProgramCustomAttribute(base.Test):
  @staticmethod
  def enter_test_data(modal):
    """Fills out all fields in the lhn_modal

    Args:
        modal (lib.page.widget.custom_attribute.NewCustomAttributeModal)
    """
    modal.enter_title(modal_custom_attribute.Program.TITLE)
    modal.enter_inline_help(modal_custom_attribute.Program.INLINE_HELP)
    modal.enter_placeholder(modal_custom_attribute.Program.PLACEHOLDER)
