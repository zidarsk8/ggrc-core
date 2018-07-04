# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""This module contains hooks for issue tracker integration."""


import assessment_integration


def init_hook():
  assessment_integration.init_hook()
