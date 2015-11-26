# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

import unittest

from ggrc import app  # noqa
from ggrc import converters
from ggrc.converters import import_helper
from ggrc.converters import column_handlers


class TestGetObjectColumnDefinitons(unittest.TestCase):

  def test_object_column_handlers(self):

    def test_single_object(obj):
      handlers = column_handlers.COLUMN_HANDLERS
      column_definitions = import_helper.get_object_column_definitions(obj)
      for key, value in column_definitions.items():
        if key in handlers:
          self.assertEqual(
              value["handler"],
              handlers[key],
              "Object '{}', column '{}': expected {}, found {}".format(
                  obj.__name__,
                  key,
                  handlers[key].__name__,
                  value["handler"].__name__,
              )
          )


    verificationErrors = []
    for obj in set(converters.get_exportables().values()):
      try:
        test_single_object(obj)
      except AssertionError as e:
        verificationErrors.append(str(e))

    verificationErrors.sort()
    self.assertEqual(verificationErrors, [])
