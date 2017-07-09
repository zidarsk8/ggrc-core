# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Base module for locust setup tasks."""

import random
import sys

import locust

from performance import base
from performance import generator

random.seed(1)


class SetUpBaseTask(base.BaseTaskSet):
  """Base class for locust setup tasks."""

  # programs = program_count
  # audits = programs * audit_count
  # assessment templates = audits * template_models * template_count
  # assessments = audits * assessment_models * assessment_count
  # custom attribute definitions = attributable_models * prefixes * cad types

  # Example setup

  _object_count = 1  # number of each normal object types
  _user_count = 1  # number of users for each global user role
  # prefixes for global CAD names for every CAD type. Prefix "2" marks CAD as
  # mandatory.
  _cad_prefixes = ["1"]

  _program_count = 1
  _program_mapping_count = 1  # max number of mappings for each mapping model
  _program_mapping_models = [
      "Control",
      "Regulation",
      "Market",
      "Objective",
      "Facility",
  ]

  # number of audits per program for one tenth of all programs
  _audit_count = 1

  # number of AT for each AT model on each audit
  _assessment_template_count = 1
  _assessment_template_models = [
      "Control",
      "Objective",
      "Facility",
      "Regulation",
      "OrgGroup",
      "Market",
  ]

  # number of generated assessments for each model on every audit. The template
  # for the given model is randomly selected
  _generated_assessment_counts = 1
  _generated_assessment_models = [
      "Control",
      "Objective",
  ]

  def set_up(self):
    super(SetUpBaseTask, self).set_up()

    if len(self.cads) < 5:
      self.create_cads(prefixes=self._cad_prefixes)
    if len(self.objects["Person"]) < 5:
      self.create_people(count=self._user_count)

    count = self._object_count
    self.create_facilities(count=count, batch_size=count)
    self.create_controls(count=count, batch_size=count)
    self.create_markets(count=count, batch_size=count)
    self.create_objectives(count=count, batch_size=count)
    self.create_regulations(count=count, batch_size=count)
    self.create_org_groups(count=count, batch_size=count)

    self.create_programs_with_mappings(
        models_=self._program_mapping_models,
        mapping_count=self._program_mapping_count,
        count=self._program_count,
    )

    programs = generator.random_objects(
        "Program",
        (len(self.objects["Program"]) + 9) / 10,
        self.objects
    )
    self.create_audits(
        programs=programs,
        count=self._audit_count
    )

    self.create_at(
        audits=self.objects["Audit"],
        at_models=self._assessment_template_models,
        count=self._assessment_template_count,
    )
    self.autogenerate_assessments(
        audits=self.objects["Audit"],
        template_models=self._generated_assessment_models,
        count=self._generated_assessment_counts,
    )
    sys.exit(0)


class WebsiteUser(locust.HttpLocust):
  """Locust http task runner."""
  # pylint: disable=too-few-public-methods
  task_set = SetUpBaseTask
  min_wait = 2000
  max_wait = 2000
