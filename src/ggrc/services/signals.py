# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: urban@reciprocitylabs.com
# Maintained By: urban@reciprocitylabs.com

"""Module for general purpose signaling"""


from blinker import Namespace


class Signals(object):
  """Class storing various general purpose signals

  Class storing various general purposse non-RESTful signals
  (see ggrc.services.common.Resource for those).
  """
  # pylint: disable=too-few-public-methods
  signals = Namespace()

  custom_attribute_changed = signals.signal(
      "Custom Attribute updated",
      """
      Indicates that a custom attribute was successfully saved to database.

        :obj: The model instance
        :value: New custom attribute value
        :service: The instance of model handling the Custom Attribute update
          operation
      """,
  )
