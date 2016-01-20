# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

import random
import collections
from datetime import date
from integration.ggrc import TestCase

import os
from freezegun import freeze_time
from ggrc_workflows.models import Workflow, TaskGroup
from integration.ggrc.api_helper import Api
from ggrc.models import program
from ggrc.models import all_models
from ggrc_workflows import models


class TestWorkflowState(TestCase):

  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_get_state(self):

    def get_state(objs):
      priority_states = collections.OrderedDict([
          # The first True state will be returned
          ("Overdue", False),
          ("InProgress", False),
          ("Finished", False),
          ("Assigned", False),
          ("Verified", False)
      ])

      for obj in objs:
        today = date.today()
        cycle = obj if isinstance(obj, models.Cycle) else obj.cycle
        if not cycle.is_current:
          continue
        for task in obj.cycle_task_group_object_tasks:
          if (task.end_date and task.end_date <= today and
                  task.status != "Verified"):
            priority_states["Overdue"] = True
        if not obj.status:
          priority_states["Assigned"] = True
        priority_states[obj.status] = True

      for state in priority_states.keys():
        if priority_states[state]:
          return state

      return None

    def workflow_state(obj):
      if isinstance(obj, models.Workflow):
        return get_state(obj.cycles)
      else:
        return get_state(obj.cycle_task_group_objects)

    states = []
    workflow_models = [model for model in all_models.all_models if
                       hasattr(model, "workflow_state")]

    dates = [
        "2016-01-19 20:39:20",
        "2015-11-17 16:39:20",
        "2016-01-29 22:39:20",
        "2015-12-02 18:39:20",
    ]
    for date_string in dates:
      with freeze_time(date_string):
        for model in workflow_models:
          # if model.__name__ != "Program":
          #   continue
          all_objects = model.query.all()
          print len(all_objects)
          for obj in all_objects:
            self.assertEqual(
                workflow_state(obj),
                obj.workflow_state,
                "{} {} {} {}".format(workflow_state(obj),obj.workflow_state, obj.id, obj.type)
            )
