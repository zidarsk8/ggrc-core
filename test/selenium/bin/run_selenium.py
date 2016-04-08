#!/usr/bin/env python2.7
# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

""" Basic selenium test runner

This script is used for running all selenium tests against the server defined
in the configuration yaml file. The script will wait a defined time for the
server to start before running the test. If the server fails to start before
its grace time is up, the script will return with an error code of 3. Error
codes 1 and 2 are reserved by pytest and status 0 is returned only if all the
tests pass.
"""

import os
import sys
import time
import urllib

import pytest   # pylint: disable=import-error

# add src to path so that we can do imports from our src
PROJECT_ROOT_PATH = os.path.dirname(os.path.abspath(__file__)) + "/../"
sys.path.append(PROJECT_ROOT_PATH + "src")

from lib import file_ops  # NOQA
from lib import environment  # NOQA


def wait_for_server():
  """ Wait for the server to return a 200 response
  """
  sys.stdout.write("Wating on server: ")
  for _ in xrange(environment.SERVER_WAIT_TIME):
    try:
      if urllib.urlopen(environment.APP_URL).getcode() == 200:
        print "[Done]"
        return True
    except IOError:
      sys.stdout.write(".")
      sys.stdout.flush()
      time.sleep(1)
  print "[Failed]"
  return False


if __name__ == "__main__":
  if not wait_for_server():
    sys.exit(3)

  file_ops.create_directory(environment.LOG_PATH)
  file_ops.delete_directory_contents(environment.LOG_PATH)

  sys.exit(pytest.main())
