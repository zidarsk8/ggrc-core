# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>


class Section(object):
  APP = "webapp"
  LOGGING = "logging"
  PYTEST = "pytest"


class Values(object):
  WAIT_FOR_APP_SERVER = "wait_for_app_server"
  BASE_URL = "base_url"
  PORT = "port"
  LEVEL = "level"
  FORMAT = "format"
  RERUN_FAILED_TEST = "rerun_failed_test"
