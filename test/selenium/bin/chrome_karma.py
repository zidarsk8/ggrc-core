# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

"""Chrome launcher for karma tests.
"""

from selenium import webdriver
import time

WAIT_PERIOD = 600
DEV_KARMA_URL = "http://dev:9876"


def open_karma_link():
  """This function is used for starting a chrome window.

  This function opens a connection the dev server on the 9876 port on which the
  karma test runner is listening. It waits up to ten minutes for the karma
  tests to finish, befor shutting down.
  """
  browser = webdriver.Chrome()
  browser.get(DEV_KARMA_URL)
  time.sleep(WAIT_PERIOD)


if __name__ == "__main__":
  open_karma_link()
