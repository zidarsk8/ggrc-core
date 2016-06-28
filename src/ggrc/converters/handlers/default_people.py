# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Handlers for default people fields in assessment templates.

These should be used on default verifiers and default assessors.
"""

from flask import current_app
from flask import json

from ggrc.models import AssessmentTemplate
from ggrc.converters import errors
from ggrc.converters.handlers import handlers


class DefaultPersonColumnHandler(handlers.ColumnHandler):
  """Handler for default verifiers and assessors."""

  KEY_MAP = {
      "default_assessors": "assessors",
      "default_verifier": "verifiers",
  }

  PEOPLE_LABELS_MAP = {
      display_name.lower(): value
      for value, display_name
      in AssessmentTemplate.DEFAULT_PEOPLE_LABELS.items()
  }

  def _parse_email_values(self):
    """Parse an email list of default assessors.

    This is the "other" option in the default assessor dropdown menu.
    """
    self.add_error(errors.UNSUPPORTED_LIST_ERROR,
                   column_name=self.display_name,
                   value_type="email lists")

  def _parse_label_values(self):
    """Parse predefined default assessors.

    These values are the normal selection in the default assessor dropdown.
    """
    value = self.PEOPLE_LABELS_MAP.get(self.raw_value.strip().lower())
    if not value:
      self.add_error(errors.WRONG_REQUIRED_VALUE,
                     column_name=self.display_name,
                     value=self.raw_value.strip().lower())
    return value

  def parse_item(self):
    """Parse values for default assessors."""

    current_app.logger.debug("%s parse item: %s", self.key, self.raw_value)

    if "@" in self.raw_value:
      return self._parse_email_values()
    else:
      return self._parse_label_values()

    current_app.logger.debug("%s parsed value: %s", self.key, self.value)

  def _get_inital_people(self):
    """Get the default_people dict from current object."""
    if self.row_converter.obj.default_people is None:
      return {}
    value = json.loads(self.row_converter.obj.default_people)
    return value

  def set_obj_attr(self):
    """Set default_people attribute.

    This is a joint function for default assessors and verifiers. The first
    column that gets handled will save the value to "_default_people" and the
    second column that gets handled will take that value, include it with its
    own and store it into the correct "default_people" field.

    NOTE: This is a temporary hack that that should be refactored once this
    code is merged into the develop branch. The joining of default_assessors
    and default_verifiers should be done by pre_commit_checks for imports.
    """
    current_app.logger.debug("%s set obj attr: %s", self.key, self.value)
    if not self.value or self.row_converter.ignore:
      return

    default_people = self._get_inital_people()
    default_people[self.KEY_MAP[self.key]] = self.value

    _default_people = getattr(self.row_converter.obj, "_default_people", {})

    if _default_people:
      default_people.update(_default_people)
      setattr(self.row_converter.obj, "default_people",
              json.dumps(default_people))
    else:
      setattr(self.row_converter.obj, "_default_people", default_people)
