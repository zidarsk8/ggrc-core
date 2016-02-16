# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com
"""Here we import all settings from config files"""

import os
import logging
from ast import literal_eval
from lib import constants, file_ops

PROJECT_ROOT_PATH = os.path.dirname(os.path.abspath(__file__)) + "/../../../"
VIRTENV_PATH = PROJECT_ROOT_PATH + constants.path.VIRTUALENV_DIR

_CONFIG_FILE_PATH = PROJECT_ROOT_PATH + constants.path.RESOURCES \
    + constants.path.YAML
_YAML = file_ops.load_yaml_contents(_CONFIG_FILE_PATH)
LOGGING_FORMAT = _YAML[constants.yaml.LOGGING][constants.yaml.FORMAT]
LOGGING_LEVEL = _YAML[constants.yaml.LOGGING][constants.yaml.LEVEL]
CHROME_DRIVER_PATH = _YAML[constants.yaml.WEBDRIVER][constants.yaml.PATH]

_YAML_APP_URL = _YAML[constants.yaml.APP][constants.yaml.URL]
APP_URL = _YAML_APP_URL \
    if _YAML_APP_URL.endswith("/") \
    else _YAML_APP_URL.join("/")
SERVER_WAIT_TIME = _YAML[constants.yaml.APP][constants.yaml.WAIT_TIME]
DISPLAY_WINDOWS = _YAML[constants.yaml.BROWSER][constants.yaml.DISPLAY]
WINDOW_RESOLUTION = literal_eval(
    _YAML[constants.yaml.BROWSER][constants.yaml.RESOLUTION])

LOG_PATH = PROJECT_ROOT_PATH + constants.path.LOGS_DIR
# register loggers
selenium_logger = logging.getLogger(constants.log.SELENIUM_REMOTE_CONNECTION)

# Only display possible problems
selenium_logger.setLevel(logging.DEBUG)
