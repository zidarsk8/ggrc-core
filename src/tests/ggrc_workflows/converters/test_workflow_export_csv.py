# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

from os.path import abspath, dirname, join
from flask.json import dumps

from ggrc.app import app
from ggrc_workflows.models import Workflow
from tests.ggrc import TestCase
from tests.ggrc_workflows.generator import WorkflowsGenerator

THIS_ABS_PATH = abspath(dirname(__file__))
CSV_DIR = join(THIS_ABS_PATH, 'test_csvs/')


class TestExportEmptyTemplate(TestCase):

  def setUp(self):
    self.client.get("/login")
    self.headers = {
        'Content-Type': 'application/json',
        "X-Requested-By": "gGRC",
        "X-export-view": "blocks",
    }

  def test_basic_policy_template(self):
    data = [{"object_name": "Workflow", "fields": "all"}]

    response = self.client.post("/_service/export_csv",
                                data=dumps(data), headers=self.headers)
    self.assertEqual(response.status_code, 200)
    self.assertIn("Title*", response.data)

  def test_multiple_empty_objects(self):
    data = [
        {"object_name": "Workflow", "fields": "all"},
        {"object_name": "TaskGroup", "fields": "all"},
        {"object_name": "TaskGroupTask", "fields": "all"},
        {"object_name": "Cycle", "fields": "all"},
        {"object_name": "CycleTaskGroup", "fields": "all"},
        {"object_name": "CycleTaskGroupObjectTask", "fields": "all"},
    ]

    response = self.client.post("/_service/export_csv",
                                data=dumps(data), headers=self.headers)
    self.assertEqual(response.status_code, 200)
    self.assertIn("Workflow", response.data)
    self.assertIn("Task Group", response.data)
    self.assertIn("Task", response.data)
    self.assertIn("Cycle", response.data)
    self.assertIn("Cycle Task", response.data)
    self.assertIn("Cycle Object", response.data)


class TestExportMultipleObjects(TestCase):

  @classmethod
  def setUpClass(cls):
    TestCase.clear_data()
    cls.tc = app.test_client()
    cls.tc.get("/login")
    cls.import_file("data_for_workflow_export_testing.csv")

  @classmethod
  def import_file(cls, filename, dry_run=False):
    data = {"file": (open(join(CSV_DIR, filename)), filename)}
    headers = {
        "X-test-only": "true" if dry_run else "false",
        "X-requested-by": "gGRC",
    }
    cls.tc.post("/_service/import_csv",
                data=data, headers=headers)

  def activate(self):
    """ activate workflows just once after the class has been initialized

    This should be in setUpClass method, but we can't access the server
    context from there."""
    gen = WorkflowsGenerator()

    # generate cycle for the only one time wf
    wf1 = Workflow.query.filter_by(status="Draft", title="wf-1").first()
    if wf1:
      gen.generate_cycle(wf1)

    workflows = Workflow.query.filter_by(status="Draft").all()
    for wf in workflows:
      gen.activate_workflow(wf)

  def setUp(self):
    self.client.get("/login")
    self.headers = {
        'Content-Type': 'application/json',
        "X-Requested-By": "gGRC",
        "X-export-view": "blocks",
    }
    self.activate()

  def export_csv(self, data):
    response = self.client.post("/_service/export_csv", data=dumps(data),
                                headers=self.headers)
    self.assert200(response)
    return response

  def test_workflow_task_group_mapping(self):
    data = [
        {
            "object_name": "Workflow",  # wf-1
            "filters": {
                "expression": {
                    "op": {"name": "relevant"},
                    "object_name": "TaskGroup",
                    "slugs": ["tg-1"],
                },
            },
            "fields": "all",
        }, {
            "object_name": "TaskGroup",  # tg-1, tg-2
            "filters": {
                "expression": {
                    "op": {"name": "relevant"},
                    "object_name": "__previous__",
                    "ids": ["0"],
                },
            },
            "fields": "all",
        },
    ]
    response = self.export_csv(data).data
    self.assertEquals(4, response.count("wf-1"))  # 2 for wf and 1 on each tg
    self.assertIn("tg-1", response)
    self.assertIn("tg-6", response)

  def test_workflow_cycle_mapping(self):
    data = [
        {
            "object_name": "Cycle",  # cycle with title wf-1
            "filters": {
                "expression": {
                    "op": {"name": "relevant"},
                    "object_name": "Workflow",
                    "slugs": ["wf-1"],
                },
            },
            "fields": "all",
        }, {
            "object_name": "Workflow",  # wf-1
            "filters": {
                "expression": {
                    "op": {"name": "relevant"},
                    "object_name": "__previous__",
                    "ids": ["0"],
                },
            },
            "fields": "all",
        },
    ]
    response = self.export_csv(data).data
    print response
    self.assertEquals(3, response.count("wf-1"))  # 1 for cycle and 2 for wf
    self.assertIn("CYCLE-", response)


