# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""Module containing decorators"""

import time
import logging
from functools import wraps

from lib import exception
from lib import environment
from lib import constants
from lib import file_ops
from lib.utils import selenium_utils

logger = logging.getLogger(__name__)


def take_screenshot_on_error(fun):
  """Decorates methods and makes a screenshot on any exception"""
  # todo: replace with pytest-selenium which automagically takes

  def wrapper(self, *args):
    try:
      return fun(self, *args)
    except Exception as e:
      logger.error(e)

      file_path = environment.LOG_PATH\
          + self.__class__.__name__\
          + "."\
          + self._driver.title
      unique_file_path = file_ops.get_unique_postfix(file_path, ".png")
      self._driver.get_screenshot_as_file(unique_file_path)
      raise

  return wrapper


def wait_for_redirect(fun):
  """Decorates methods and waits until url has changed"""
  @wraps(fun)
  def wrapper(self, *args, **kwargs):
    from_url = self._driver.current_url
    result = fun(self, *args, **kwargs)

    timer_start = time.time()

    while from_url == self._driver.current_url:
      time.sleep(0.1)

      if time.time() - timer_start > constants.ux.MAX_USER_WAIT_SECONDS:
        raise exception.RedirectTimeout(
            "Failed to redirect from {} to {}".format(
                from_url, self._driver.current_url))

    return result
  return wrapper


def handle_alert(fun):
  """Accepts or dismisses an alert"""
  @wraps(fun)
  def wrapper(self, *args, **kwargs):
    result = fun(self, *args, **kwargs)
    selenium_utils.handle_alert(self._driver, accept=True)
    return result
  return wrapper
