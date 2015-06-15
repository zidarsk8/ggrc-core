# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: urban@reciprocitylabs.com
# Maintained By: urban@reciprocitylabs.com

import random
import copy
from tests.ggrc import TestCase

import os
from ggrc import db
from ggrc_workflows.models import Workflow, TaskGroup, CycleTaskGroupObjectTask, Cycle
from tests.ggrc_workflows.generator import WorkflowsGenerator
from tests.ggrc.api_helper import Api
from tests.ggrc.generator import ObjectGenerator
from nose.plugins.skip import SkipTest


if os.environ.get('TRAVIS', False):
  random.seed(1)  # so we can reproduce the tests if needed


class BaseWorkflowTestCase(TestCase):
  def setUp(self):
    TestCase.setUp(self)
    self.api = Api()
    self.generator = WorkflowsGenerator()
    self.object_generator = ObjectGenerator()

    self.random_objects = self.object_generator.generate_random_objects()
    self.create_test_cases()

  def tearDown(self):
    pass

  def create_test_cases(self):
    self.quarterly_wf_1 = {
      "title": "quarterly wf 1",
      "description": "",
      "frequency": "quarterly",
      "task_groups": [{
                        "title": "tg_1",
                        "task_group_tasks": [{
                                               "description": self.generator.random_str(100),
                                               "relative_start_day": 5,
                                               "relative_start_month": 1,
                                               "relative_end_day": 25,
                                               "relative_end_month": 2,
                                               }, {
                                               "description": self.generator.random_str(100),
                                               "relative_start_day": 15,
                                               "relative_start_month": 2,
                                               "relative_end_day": 28,
                                               "relative_end_month": 2,
                                               }, {
                                               "description": self.generator.random_str(100),
                                               "relative_start_day": 1,
                                               "relative_start_month": 1,
                                               "relative_end_day": 1,
                                               "relative_end_month": 1,
                                               },
                                             ],
                        },
                      ]
    }

    self.weekly_wf_1 = {
      "title": "weekly thingy",
      "description": "start this many a time",
      "frequency": "weekly",
      "task_groups": [{
                        "title": "tg_2",
                        "task_group_tasks": [{
                                               "description": self.generator.random_str(100),
                                               "relative_end_day": 1,
                                               "relative_end_month": None,
                                               "relative_start_day": 5,
                                               "relative_start_month": None,
                                               }, {
                                               "title": "monday task",
                                               "relative_end_day": 1,
                                               "relative_end_month": None,
                                               "relative_start_day": 1,
                                               "relative_start_month": None,
                                               }, {
                                               "title": "weekend task",
                                               "relative_end_day": 4,
                                               "relative_end_month": None,
                                               "relative_start_day": 1,
                                               "relative_start_month": None,
                                               },
                                             ],
                        "task_group_objects": self.random_objects
                      },
                      ]
    }

    self.one_time_workflow_1 = {
      "title": "one time wf test",
      "description": "some test workflow",
      "task_groups": [{
                        "title": "tg_1",
                        "task_group_tasks": [{}, {}, {}]
                      }, {
                        "title": "tg_2",
                        "task_group_tasks": [{
                                               "description": self.generator.random_str(100)
                                             }, {}
                        ],
                        "task_group_objects": self.random_objects[:2]
                      }, {
                        "title": "tg_3",
                        "task_group_tasks": [{
                                               "title": "simple task 1",
                                               "description": self.generator.random_str(100)
                                             }, {
                                               "title": self.generator.random_str(),
                                               "description": self.generator.random_str(100)
                                             }, {
                                               "title": self.generator.random_str(),
                                               "description": self.generator.random_str(100)
                                             }
                        ],
                        "task_group_objects": self.random_objects
                      }
      ]
    }
    self.one_time_workflow_2 = {
      "title": "test_wf_title",
      "description": "some test workflow",
      "task_groups": [{
                        "title": "tg_1",
                        "task_group_tasks": [{}, {}, {}]
                      },
                      {"title": "tg_2",
                       "task_group_tasks": [{
                                              "description": self.generator.random_str(100)
                                            },
                         {}
                       ],
                       "task_group_objects": self.random_objects[:2]
                       },
                      {"title": "tg_3",
                       "task_group_tasks": [{
                                              "title": "simple task 1",
                                              "description": self.generator.random_str(100)
                                            }, {
                                              "title": self.generator.random_str(),
                                              "description": self.generator.random_str(100)
                                            }, {
                                              "title": self.generator.random_str(),
                                              "description": self.generator.random_str(100)
                                            }],
                       "task_group_objects": []
                       }
      ]
    }

    self.monthly_workflow_1 = {
      "title": "monthly test wf",
      "description": "start this many a time",
      "frequency": "monthly",
      "task_groups": [
        {"title": "tg_2",
         "task_group_tasks": [{
                                "description": self.generator.random_str(100),
                                "relative_end_day": 1,
                                "relative_end_month": None,
                                "relative_start_day": 5,
                                "relative_start_month": None,
                                },
                              {"title": "monday task",
                               "relative_end_day": 1,
                               "relative_end_month": None,
                               "relative_start_day": 1,
                               "relative_start_month": None,
                               },
                              {"title": "weekend task",
                               "relative_end_day": 4,
                               "relative_end_month": None,
                               "relative_start_day": 1,
                               "relative_start_month": None,
                               },
                              ],
         "task_group_objects": self.random_objects
         },
        ]
    }
    self.all_workflows = [
      self.one_time_workflow_1,
      self.one_time_workflow_2,
      self.weekly_wf_1,
      self.monthly_workflow_1,
      self.quarterly_wf_1,
      ]
