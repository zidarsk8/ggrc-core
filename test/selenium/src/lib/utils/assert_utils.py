# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Assert utils."""


class SoftAssert(object):
  """Class for performing soft asserts."""

  def __init__(self):
    self.__errors = []

  def expect(self, expr, msg):
    """Tries to perform assert and if fails stores msg into errors list."""
    try:
      assert expr, msg
    except AssertionError:
      self.__errors.append(msg)

  def assert_expectations(self):
    """Performs assert that there were no soft_assert errors."""
    assert not self.__errors, ("There were some errors during soft_assert:\n"
                               "{}".format(self.__errors))
