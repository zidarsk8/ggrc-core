# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module contains integration tests for Cycle Task Group Object Task Object
updates via import"""

# pylint: disable=invalid-name

from os.path import join
from os.path import abspath
from os.path import dirname
from freezegun import freeze_time

from ggrc import db
from ggrc.converters import errors
from ggrc_workflows import start_recurring_cycles
from ggrc_workflows.models import CycleTaskGroupObjectTask
from integration.ggrc.converters import TestCase
from integration.ggrc_workflows.generator import WorkflowsGenerator
from integration.ggrc.generator import ObjectGenerator


# pylint: disable=too-many-instance-attributes
class TestCycleTaskGroupObjectTaskUpdate(TestCase):

  """ This class contains simple cycle_task_group_object_task update tests
  using import functionality
  """

  CSV_DIR = join(abspath(dirname(__file__)), "test_csvs/")

  def setUp(self):
    TestCase.setUp(self)
    self.wf_generator = WorkflowsGenerator()
    self.object_generator = ObjectGenerator()

    self.random_objects = self.object_generator.generate_random_objects()
    _, self.person_1 = self.object_generator.generate_person(
        user_role="Administrator")
    _, self.person_2 = self.object_generator.generate_person(
        user_role="Administrator")
    self._create_test_cases()

  def _cmp_tasks(self, exp_tasks):
    """Compare tasks values from argument's list and test DB."""
    for exp_slug, exp_task in exp_tasks.iteritems():
      res_task = db.session.query(CycleTaskGroupObjectTask).filter_by(
          slug=exp_slug).first()
      for attr, val in exp_task.iteritems():
        self.assertEqual(str(getattr(res_task, attr, None)), val)

  def test_cycle_task_group_object_task_update(self):
    """Test cycle task group object task update via import"""
    with freeze_time("2016-10-02"):
      # Generate Workflow, Task Groups and Cycle Task Group Object Tasks
      # objects
      _, workflow = self.wf_generator.generate_workflow(self.test_workflow)
      self.wf_generator.activate_workflow(workflow)
      start_recurring_cycles()
      # First test: update 4 tasks with correct CSV import
      self._cmp_tasks(self.exp_tasks_before_update)
      filename = "cycle_task_group_object_task_active_update.csv"
      response = self.import_file(filename)
      expected_errors = {
          "Cycle Task Group Object Task": {
              "block_warnings": {
                  errors.NON_IMPORTABLE_COLUMN_WARNING.format(
                      line=2,
                      column_name='state',
                  ),
              }
          }
      }
      self._check_csv_response(response, expected_errors)
      self._cmp_tasks(self.exp_tasks_after_update)

  def _create_test_cases(self):
    """Create test cases data"""
    def person_dict(person_id):
      """Return person data"""
      return {
          "href": "/api/people/%d" % person_id,
          "id": person_id,
          "type": "Person"
      }

    self.exp_tasks_before_update = {
        "CYCLETASK-1": {
            "title": "task 1 in tg 1",
            "description": "descr task 1 in tg 1",
            "start_date": "2016-09-30",
            "end_date": "2016-10-07",
            "finished_date": "None",
            "verified_date": "None",
            "status": "Assigned"
        },
        "CYCLETASK-2": {
            "title": "task 2 in tg 1",
            "description": "descr task 2 in tg 1",
            "start_date": "2016-10-07",
            "end_date": "2016-10-14",
            "finished_date": "None",
            "verified_date": "None",
            "status": "Assigned"
        },
        "CYCLETASK-3": {
            "title": "task 1 in tg 2",
            "description": "descr task 1 in tg 2",
            "start_date": "2016-10-14",
            "end_date": "2016-10-21",
            "finished_date": "None",
            "verified_date": "None",
            "status": "Assigned"
        },
        "CYCLETASK-4": {
            "title": "task 2 in tg 2",
            "description": "descr task 2 in tg 2",
            "start_date": "2016-10-21",
            "end_date": "2016-10-31",
            "finished_date": "None",
            "verified_date": "None",
            "status": "Assigned"
        }
    }

    self.test_workflow = {
        "title": "test cycle_task_group_object_task update",
        "notify_on_change": False,
        "description": "test workflow",
        "owners": [person_dict(self.person_2.id)],
        "frequency": "monthly",
        "task_groups": [{
            "title": "task group 1",
            "contact": person_dict(self.person_1.id),
            "task_group_tasks": [{
                "title": self.exp_tasks_before_update["CYCLETASK-1"]["title"],
                "description":
                    self.exp_tasks_before_update["CYCLETASK-1"]["description"],
                "contact": person_dict(self.person_1.id),
                "relative_start_day": 2,
                "relative_end_day": 8,
            }, {
                "title": self.exp_tasks_before_update["CYCLETASK-2"]["title"],
                "description":
                    self.exp_tasks_before_update["CYCLETASK-2"]["description"],
                "contact": person_dict(self.person_1.id),
                "relative_start_day": 9,
                "relative_end_day": 15,
            }],
            "task_group_objects": self.random_objects[:2]
        }, {
            "title": "another one time task group",
            "contact": person_dict(self.person_1.id),
            "task_group_tasks": [{
                "title": self.exp_tasks_before_update["CYCLETASK-3"]["title"],
                "description":
                    self.exp_tasks_before_update["CYCLETASK-3"]["description"],
                "contact": person_dict(self.person_1.id),
                "relative_start_day": 16,
                "relative_end_day": 22,
            }, {
                "title": self.exp_tasks_before_update["CYCLETASK-4"]["title"],
                "description":
                    self.exp_tasks_before_update["CYCLETASK-4"]["description"],
                "contact": person_dict(self.person_2.id),
                "relative_start_day": 23,
                "relative_end_day": 31,
            }],
            "task_group_objects": []
        }]
    }

    self.exp_tasks_after_update = {
        "CYCLETASK-1": {
            "title": "first task in task group 1",
            "description": "details 1",
            "start_date": "2016-11-01",
            "end_date": "2016-11-05",
            "finished_date": "None",
            "verified_date": "None",
            "status": "Assigned"
        },
        "CYCLETASK-2": {
            "title": "second task in task group 1",
            "description": "details 2",
            "start_date": "2016-11-06",
            "end_date": "2016-11-10",
            "finished_date": "None",
            "verified_date": "None",
            "status": "Assigned"
        },
        "CYCLETASK-3": {
            "title": "first task in task group 2",
            "description": "details 3",
            "start_date": "2016-11-11",
            "end_date": "2016-11-18",
            "finished_date": "None",
            "verified_date": "None",
            "status": "Assigned"
        },
        "CYCLETASK-4": {
            "title": "second task in task group 2",
            "description": "details 4",
            "start_date": "2016-11-19",
            "end_date": "2016-11-30",
            "finished_date": "None",
            "verified_date": "None",
            "status": "Assigned"
        }
    }
