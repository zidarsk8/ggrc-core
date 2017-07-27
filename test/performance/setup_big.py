# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module for the big setup task."""

import random

import locust

from performance import setup_base

random.seed(1)


class BigSetup(setup_base.SetUpBaseTask):
  """Big setup task.

  For property and number descriptions see the super class.
  """

  _object_count = 2000
  _user_count = 60
  _cad_prefixes = ["1"]

  _program_count = 50
  _program_mapping_count = 500
  _program_mapping_models = [
      "Control",
      "Regulation",
      "Market",
      "Objective",
      "Facility",
  ]

  _audit_count = 2

  _assessment_template_count = 3
  _assessment_template_models = [
      "Control",
      "Objective",
      "Facility",
      "Regulation",
      "OrgGroup",
      "Market",
  ]

  _generated_assessment_counts = 100
  _generated_assessment_models = [
      "Control",
      "Objective",
      "Regulation",
  ]


class WebsiteUser(locust.HttpLocust):
  """Locust http task runner."""
  # pylint: disable=too-few-public-methods
  task_set = BigSetup
  min_wait = 2000
  max_wait = 2000
