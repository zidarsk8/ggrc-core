# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Contains ValidateOnComplete mixin.

This defines a procedure of an object's validation when its status moves from
one of NOT_DONE_STATES to DONE_STATES.
"""
from ggrc.models.utils import validate_assessment_done_state


class ValidateOnComplete(object):  # pylint: disable=too-few-public-methods
  """Defines the validation routine before marking an object as complete.

  Requires Stateful and Statusable to be mixed in as well."""

  skip_validation = False

  @staticmethod
  def validate_done_state(old_value, obj):
    """Check if it's allowed to set done state from not done.

    Args:
        old_value: Old state (Assessment.VALID_STATES).

    Raise:
        ValidationError if state can't be changed.
    """
    validate_assessment_done_state(old_value, obj)
