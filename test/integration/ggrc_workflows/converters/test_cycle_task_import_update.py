# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module contains integration tests for Cycle Task Group Object Task Object
updates via import"""

# pylint: disable=invalid-name
import datetime
from collections import OrderedDict

from os.path import join
from os.path import abspath
from os.path import dirname
import mock
from freezegun import freeze_time

import ddt

from ggrc import db
from ggrc.models import all_models
from ggrc.converters import errors
from ggrc_workflows.models import Cycle
from ggrc_workflows.models import CycleTaskGroupObjectTask
from integration.ggrc_workflows.models import factories
from integration.ggrc.models import factories as ggrc_factories
from integration.ggrc import TestCase
from integration.ggrc.generator import ObjectGenerator
from integration.ggrc_workflows.generator import WorkflowsGenerator


class BaseTestCycleTaskImportUpdate(TestCase):

  @staticmethod
  def generate_expected_warning(*columns):
    return {
        'Cycle Task': {
            'block_warnings': {
                errors.ONLY_IMPORTABLE_COLUMNS_WARNING.format(
                    line=2,
                    columns=", ".join(columns)
                )
            },
        }
    }


# pylint: disable=too-many-instance-attributes
class TestCycleTaskImportUpdate(BaseTestCycleTaskImportUpdate):

  """ This class contains simple cycle task update tests using import
  functionality
  """

  CSV_DIR = join(abspath(dirname(__file__)), "test_csvs/")

  IMPORTABLE_COLUMN_NAMES = [
      "Summary",
      "Task Details",
      "Start Date", "Due Date",
      "Actual Finish Date",
      "Actual Verified Date",
      "State",
      "Task Assignees",
  ]

  def setUp(self):
    super(TestCycleTaskImportUpdate, self).setUp()
    self.wf_generator = WorkflowsGenerator()
    self.object_generator = ObjectGenerator()
    self.random_objects = self.object_generator.generate_random_objects(2)
    _, self.person_1 = self.object_generator.generate_person(
        user_role="Administrator")
    self.ftime_active = "2016-07-01"
    self.ftime_historical = "2014-05-01"
    self._create_test_cases_data()
    # It is needed because cycle-tasks are generated automatically with
    # 'slug' based on auto_increment 'id' field.
    # At start of each test we suppose that created cycle-task's 'slug'
    # lie in range from 1 to 10.
    db.session.execute('ALTER TABLE cycle_task_group_object_tasks '
                       'AUTO_INCREMENT = 1')

  def test_cycle_task_correct(self):
    """Test cycle task update via import with correct data"""
    self._generate_cycle_tasks()
    with freeze_time(self.ftime_active):
      response = self.import_file("cycle_task_correct.csv")
      self._check_csv_response(response, {})
      self._cmp_tasks(self.expected_cycle_task_correct)

  def test_cycle_task_warnings(self):
    """Test cycle task update via import with data which is the reason of
    warnings about non-importable columns."""
    self._generate_cycle_tasks()
    with freeze_time(self.ftime_active):
      response = self.import_file("cycle_task_warnings.csv")
      self._check_csv_response(response, self.expected_warnings)
      self._cmp_tasks(self.expected_cycle_task_correct)

  def test_cycle_task_permission_error(self):
    """Test cycle task update via import with non-admin user which is the
    reason of error. Only admin can update cycle tasks via import."""
    self._generate_cycle_tasks()
    with freeze_time(self.ftime_active):
      _, creator = self.object_generator.generate_person(user_role="Creator")
      response = self.import_file("cycle_task_correct.csv", person=creator)
      self._check_csv_response(response, self.expected_permission_error)
      # Cycle tasks' data shouldn't be changed in test DB after import run from
      # non-admin user
      expected_cycle_task_permission_error = {}
      expected_cycle_task_permission_error.update(
          self.generated_cycle_tasks_active)
      expected_cycle_task_permission_error.update(
          self.generated_cycle_tasks_historical)
      self._cmp_tasks(expected_cycle_task_permission_error)

  def _cmp_tasks(self, expected_ctasks):
    """Compare tasks values from argument's list and test DB."""
    for ctask in db.session.query(CycleTaskGroupObjectTask).all():
      if ctask.slug not in expected_ctasks:
        continue
      exp_task = expected_ctasks[ctask.slug]
      for attr, val in exp_task.iteritems():
        self.assertEqual(
            str(getattr(ctask, attr, None)),
            val,
            "attr {} value for {} not expected".format(attr, ctask.slug)
        )

  # pylint: disable=too-many-arguments
  def _activate_workflow(self, ftime, workflow, task_group, task_group_tasks,
                         random_object, cycle_tasks):
    """Helper which is responsible for active cycle-tasks creation"""
    with freeze_time(ftime):
      _, wf = self.wf_generator.generate_workflow(workflow)
      _, tg = self.wf_generator.generate_task_group(wf, task_group)
      for task in task_group_tasks:
        self.wf_generator.generate_task_group_task(tg, task)
      self.wf_generator.generate_task_group_object(tg, random_object)

      _, cycle = self.wf_generator.generate_cycle(wf)
      self.wf_generator.activate_workflow(wf)

      for exp_slug, exp_task in cycle_tasks.iteritems():
        obj = db.session.query(CycleTaskGroupObjectTask).filter_by(
            slug=exp_slug
        ).first()
        if exp_task["status"] == "Verified":
          self.wf_generator.modify_object(obj, {"status": "Finished"})
        self.wf_generator.modify_object(obj, {"status": exp_task["status"]})
    self._cmp_tasks(cycle_tasks)
    return cycle

  def _generate_cycle_tasks(self):
    """Helper which is responsible for test data creation"""
    self._activate_workflow(self.ftime_active, self.workflow_active,
                            self.task_group_active,
                            self.task_group_tasks_active,
                            self.random_objects[0],
                            self.generated_cycle_tasks_active)
    cycle = self._activate_workflow(self.ftime_historical,
                                    self.workflow_historical,
                                    self.task_group_historical,
                                    self.task_group_tasks_historical,
                                    self.random_objects[1],
                                    self.generated_cycle_tasks_historical)
    with freeze_time(self.ftime_historical):
      cycle = Cycle.query.get(cycle.id)
      self.wf_generator.modify_object(cycle, data={"is_current": False})

  def _create_test_cases_data(self):
    """Create test cases data: for object generation,
    expected data for checks"""
    def person_dict(person_id):
      """Return person data"""
      return {
          "href": "/api/people/%d" % person_id,
          "id": person_id,
          "type": "Person"
      }

    self.workflow_active = {
        "title": "workflow active title",
        "description": "workflow active description",
        "owners": [person_dict(self.person_1.id)],
        "notify_on_change": False,
    }

    self.task_group_active = {
        "title": "task group active title",
        "contact": person_dict(self.person_1.id),
    }

    self.task_group_tasks_active = [{
        "title": "task active title 1",
        "description": "task active description 1",
        "contact": person_dict(self.person_1.id),
        "start_date": "07/01/2016",
        "end_date": "07/06/2016",
    }, {
        "title": "task active title 2",
        "description": "task active description 2",
        "contact": person_dict(self.person_1.id),
        "start_date": "07/07/2016",
        "end_date": "07/12/2016",
    }, {
        "title": "task active title 3",
        "description": "task active description 3",
        "contact": person_dict(self.person_1.id),
        "start_date": "07/13/2016",
        "end_date": "07/18/2016",
    }, {
        "title": "task active title 4",
        "description": "task active description 4",
        "contact": person_dict(self.person_1.id),
        "start_date": "07/19/2016",
        "end_date": "07/24/2016",
    }, {
        "title": "task active title 5",
        "description": "task active description 5",
        "contact": person_dict(self.person_1.id),
        "start_date": "07/25/2016",
        "end_date": "07/30/2016",
    }]

    # Active cycle tasks which should be generated from previous structure
    # at the beginning of each test
    self.generated_cycle_tasks_active = {
        "CYCLETASK-1": {
            "title": self.task_group_tasks_active[0]["title"],
            "description": self.task_group_tasks_active[0]["description"],
            "start_date": "2016-07-01",
            "end_date": "2016-07-06",
            "finished_date": "None",
            "verified_date": "None",
            "status": "Assigned"
        },
        "CYCLETASK-2": {
            "title": self.task_group_tasks_active[1]["title"],
            "description": self.task_group_tasks_active[1]["description"],
            "start_date": "2016-07-07",
            "end_date": "2016-07-12",
            "finished_date": "None",
            "verified_date": "None",
            "status": "Declined"
        },
        "CYCLETASK-3": {
            "title": self.task_group_tasks_active[2]["title"],
            "description": self.task_group_tasks_active[2]["description"],
            "start_date": "2016-07-13",
            "end_date": "2016-07-18",
            "finished_date": "None",
            "verified_date": "None",
            "status": "InProgress"
        },
        "CYCLETASK-4": {
            "title": self.task_group_tasks_active[3]["title"],
            "description": self.task_group_tasks_active[3]["description"],
            "start_date": "2016-07-19",
            "end_date": "2016-07-22",
            "finished_date": "2016-07-01 00:00:00",
            "verified_date": "None",
            "status": "Finished"
        },
        "CYCLETASK-5": {
            "title": self.task_group_tasks_active[4]["title"],
            "description": self.task_group_tasks_active[4]["description"],
            "start_date": "2016-07-25",
            "end_date": "2016-07-29",
            "finished_date": "2016-07-01 00:00:00",
            "verified_date": "2016-07-01 00:00:00",
            "status": "Verified"
        }
    }

    self.workflow_historical = {
        "title": "workflow historical title",
        "description": "workflow historical description",
        "owners": [person_dict(self.person_1.id)],
        "notify_on_change": False,
    }

    self.task_group_historical = {
        "title": "task group historical title",
        "contact": person_dict(self.person_1.id),
    }

    self.task_group_tasks_historical = [{
        "title": "task historical title 1",
        "description": "task historical description 1",
        "contact": person_dict(self.person_1.id),
        "start_date": "05/01/2014",
        "end_date": "05/06/2014",
    }, {
        "title": "task historical title 2",
        "description": "task historical description 2",
        "contact": person_dict(self.person_1.id),
        "start_date": "05/07/2014",
        "end_date": "05/12/2014",
    }, {
        "title": "task historical title 3",
        "description": "task historical description 3",
        "contact": person_dict(self.person_1.id),
        "start_date": "05/13/2014",
        "end_date": "05/18/2014",
    }, {
        "title": "task historical title 4",
        "description": "task historical description 4",
        "contact": person_dict(self.person_1.id),
        "start_date": "05/19/2014",
        "end_date": "05/24/2014",
    }, {
        "title": "task historical title 5",
        "description": "task historical description 5",
        "contact": person_dict(self.person_1.id),
        "start_date": "05/25/2014",
        "end_date": "05/30/2014",
    },
    ]

    # Historical cycle tasks which should be generated from previous structure
    # at the beginning of each test.
    self.generated_cycle_tasks_historical = {
        "CYCLETASK-6": {
            "title": self.task_group_tasks_historical[0]["title"],
            "description": self.task_group_tasks_historical[0]["description"],
            "start_date": "2014-05-01",
            "end_date": "2014-05-06",
            "finished_date": "None",
            "verified_date": "None",
            "status": "Assigned"
        },
        "CYCLETASK-7": {
            "title": self.task_group_tasks_historical[1]["title"],
            "description": self.task_group_tasks_historical[1]["description"],
            "start_date": "2014-05-07",
            "end_date": "2014-05-12",
            "finished_date": "None",
            "verified_date": "None",
            "status": "Declined"
        },
        "CYCLETASK-8": {
            "title": self.task_group_tasks_historical[2]["title"],
            "description": self.task_group_tasks_historical[2]["description"],
            "start_date": "2014-05-13",
            "end_date": "2014-05-16",
            "finished_date": "None",
            "verified_date": "None",
            "status": "InProgress"
        },
        "CYCLETASK-9": {
            "title": self.task_group_tasks_historical[3]["title"],
            "description": self.task_group_tasks_historical[3]["description"],
            "start_date": "2014-05-19",
            "end_date": "2014-05-23",
            "finished_date": "2014-05-01 00:00:00",
            "verified_date": "None",
            "status": "Finished"
        },
        "CYCLETASK-10": {
            "title": self.task_group_tasks_historical[4]["title"],
            "description": self.task_group_tasks_historical[4]["description"],
            "start_date": "2014-05-23",
            "end_date": "2014-05-30",
            "finished_date": "2014-05-01 00:00:00",
            "verified_date": "2014-05-01 00:00:00",
            "status": "Verified"
        }
    }

    # Expected cycle tasks which should be created in correct cycle task update
    # case. It is needed for most tests.
    self.expected_cycle_task_correct = {
        "CYCLETASK-1": {
            "title": self.task_group_tasks_active[0]["title"] + " one",
            "description":
                self.task_group_tasks_active[0]["description"] + " one",
            "start_date": "2016-06-01",
            "end_date": "2016-06-06",
            "finished_date": "None",
            "verified_date": "None",
            "status": "Assigned"
        },
        "CYCLETASK-2": {
            "title": self.task_group_tasks_active[1]["title"] + " two",
            "description":
                self.task_group_tasks_active[1]["description"] + " two",
            "start_date": "2016-06-07",
            "end_date": "2016-06-12",
            "finished_date": "None",
            "verified_date": "None",
            "status": "Declined"
        },
        "CYCLETASK-3": {
            "title": self.task_group_tasks_active[2]["title"] + " three",
            "description":
                self.task_group_tasks_active[2]["description"] + " three",
            "start_date": "2016-06-13",
            "end_date": "2016-06-18",
            "finished_date": "None",
            "verified_date": "None",
            "status": "InProgress"
        },
        "CYCLETASK-4": {
            "title": self.task_group_tasks_active[3]["title"] + " four",
            "description":
                self.task_group_tasks_active[3]["description"] + " four",
            "start_date": "2016-06-19",
            "end_date": "2016-06-24",
            "finished_date": "2016-07-19 00:00:00",
            "verified_date": "None",
            "status": "Finished"
        },
        "CYCLETASK-5": {
            "title": self.task_group_tasks_active[4]["title"] + " five",
            "description":
                self.task_group_tasks_active[4]["description"] + " five",
            "start_date": "2016-06-25",
            "end_date": "2016-06-30",
            "finished_date": "2016-07-25 00:00:00",
            "verified_date": "2016-08-30 00:00:00",
            "status": "Verified"
        },
        "CYCLETASK-6": {
            "title": self.task_group_tasks_historical[0]["title"] + " one",
            "description":
                self.task_group_tasks_historical[0]["description"] + " one",
            "start_date": "2014-04-01",
            "end_date": "2014-04-06",
            "finished_date": "None",
            "verified_date": "None",
            "status": "Assigned"
        },
        "CYCLETASK-7": {
            "title": self.task_group_tasks_historical[1]["title"] + " two",
            "description":
                self.task_group_tasks_historical[1]["description"] + " two",
            "start_date": "2014-04-07",
            "end_date": "2014-04-12",
            "finished_date": "None",
            "verified_date": "None",
            "status": "Declined"
        },
        "CYCLETASK-8": {
            "title": self.task_group_tasks_historical[2]["title"] + " three",
            "description":
                self.task_group_tasks_historical[2]["description"] + " three",
            "start_date": "2014-04-13",
            "end_date": "2014-04-18",
            "finished_date": "None",
            "verified_date": "None",
            "status": "InProgress"
        },
        "CYCLETASK-9": {
            "title": self.task_group_tasks_historical[3]["title"] + " four",
            "description":
                self.task_group_tasks_historical[3]["description"] + " four",
            "start_date": "2014-04-19",
            "end_date": "2014-04-24",
            "finished_date": "2014-05-19 00:00:00",
            "verified_date": "None",
            "status": "Finished"
        },
        "CYCLETASK-10": {
            "title": self.task_group_tasks_historical[4]["title"] + " five",
            "description":
                self.task_group_tasks_historical[4]["description"] + " five",
            "start_date": "2014-04-25",
            "end_date": "2014-04-30",
            "finished_date": "2014-05-25 00:00:00",
            "verified_date": "2014-06-30 00:00:00",
            "status": "Verified"
        }
    }

    # Below is description of warning for non-importable columns. It is needed
    # for test_cycle_task_warnings.
    self.expected_warnings = self.generate_expected_warning(
        *self.IMPORTABLE_COLUMN_NAMES
    )

    # This is an error message which should be shown during
    # test_cycle_task_create_error test
    self.expected_create_error = {
        'Cycle Task': {
            'row_errors': {errors.CREATE_INSTANCE_ERROR.format(line=13)}
        }
    }

    # Below is expected date errors for test_cycle_task_date_error. They should
    # be shown during date validator's tests.
    self.expected_date_error = {
        'Cycle Task': {
            'row_errors': {
                errors.INVALID_START_END_DATES.format(
                    line=3,
                    start_date="Start Date",
                    end_date="End Date",
                ),
                errors.INVALID_STATUS_DATE_CORRELATION.format(
                    line=4,
                    date="Actual Finish Date",
                    status="not Finished",
                ),
                errors.INVALID_STATUS_DATE_CORRELATION.format(
                    line=6,
                    date="Actual Verified Date",
                    status="not Verified",
                ),
                errors.INVALID_START_END_DATES.format(
                    line=7,
                    start_date="Actual Finish Date",
                    end_date="Actual Verified Date",
                ),
                errors.INVALID_START_END_DATES.format(
                    line=8,
                    start_date="Start Date",
                    end_date="End Date",
                ),
            },
        }
    }
    # Below is expected cycle-tasks data which should appear in test DB after
    # test_cycle_task_date_error run
    self.expected_cycle_task_date_error = dict()
    self.expected_cycle_task_date_error.update(
        self.generated_cycle_tasks_active)
    self.expected_cycle_task_date_error.update(
        self.generated_cycle_tasks_historical)
    self.expected_cycle_task_date_error["CYCLETASK-9"] = (
        self.expected_cycle_task_correct["CYCLETASK-9"])
    self.expected_cycle_task_date_error["CYCLETASK-10"] = (
        self.expected_cycle_task_correct["CYCLETASK-10"])

    # Expected error message which should be shown after
    # test_cycle_task_permission_error run
    self.expected_permission_error = {
        'Cycle Task': {
            'block_errors': {errors.PERMISSION_ERROR.format(line=2)}
        }
    }


@ddt.ddt
class TestCycleTaskImportUpdateAssignee(BaseTestCycleTaskImportUpdate):
  """Test cases for update assignee column on import cycle tasks"""

  def setUp(self):
    self.instance = factories.CycleTaskFactory()
    self.user = ggrc_factories.PersonFactory()
    self.query = CycleTaskGroupObjectTask.query.filter(
        CycleTaskGroupObjectTask.id == self.instance.id
    )

  @ddt.data(
      "CycleTask",
      "Cycle Task",
      "Cycle_Task",
      "Cycle Task Group Object Task",
      "cycle_task_group_object_task",
      "cycletaskgroupobjecttask",
  )
  def test_update_assignee(self, alias):
    """Test update assignee for {0}"""
    assignees = list(self.get_persons_for_role_name(
        self.query.first(), "Task Assignees"))
    self.assertFalse(assignees)
    response = self.import_data(OrderedDict([
        ("object_type", alias),
        ("Code*", self.instance.slug),
        ("Task Assignees*", self.user.email),
    ]))
    self._check_csv_response(response, {})
    assignees = list(self.get_persons_for_role_name(
        self.query.first(), "Task Assignees"))
    self.assertEqual([self.user.email], [u.email for u in assignees])

  @ddt.data(
      "CycleTask",
      "Cycle Task",
      "Cycle_Task",
      "Cycle Task Group Object Task",
      "cycle_task_group_object_task",
      "cycletaskgroupobjecttask",
  )
  def test_update_assignee_with_non_importable(self, alias):
    """Test update assignee for {0} with non importable field"""
    assignees = list(
        self.get_persons_for_role_name(self.query.first(), "Task Assignees"))
    self.assertFalse(assignees)
    response = self.import_data(OrderedDict([
        ("object_type", alias),
        ("Code*", self.instance.slug),
        ("Task Assignees*", self.user.email),
        ("Task Type", "some data"),
    ]))
    assignees = list(
        self.get_persons_for_role_name(self.query.first(), "Task Assignees"))
    self.assertEqual([self.user.email], [u.email for u in assignees])
    self._check_csv_response(response,
                             self.generate_expected_warning('Task Assignees'))


@ddt.ddt
class TestCycleTaskStatusUpdate(BaseTestCycleTaskImportUpdate):
  """Test cases for update status on import cycle tasks"""

  @classmethod
  def setUpClass(cls):
    """Setup special hooks to that test class."""
    cls._current_user_wfo_or_assignee = (
        CycleTaskGroupObjectTask.current_user_wfo_or_assignee
    )
    CycleTaskGroupObjectTask.current_user_wfo_or_assignee = mock.MagicMock(
        return_value=True
    )

  @classmethod
  def tearDownClass(cls):
    CycleTaskGroupObjectTask.current_user_wfo_or_assignee = (
        cls._current_user_wfo_or_assignee
    )

  DEFAULT_TASK_STATUSES = [CycleTaskGroupObjectTask.ASSIGNED] * 3

  ALIAS = "Cycle Task"

  def setUp(self):
    with ggrc_factories.single_commit():
      self.workflow = factories.WorkflowFactory(
          status=all_models.Workflow.ACTIVE
      )
      self.cycle = factories.CycleFactory(workflow=self.workflow)
      self.group = factories.CycleTaskGroupFactory(
          cycle=self.cycle,
          context=self.cycle.workflow.context
      )
      self.tasks = []
      for ind, task_status in enumerate(self.DEFAULT_TASK_STATUSES):
        self.tasks.append(factories.CycleTaskFactory(
            title='task{}'.format(ind),
            cycle=self.cycle,
            cycle_task_group=self.group,
            context=self.cycle.workflow.context,
            status=task_status,
        ))
    # Emulate that current user is assignee for all test CycleTasks.
    self.task_ids = [t.id for t in self.tasks]

  VERIFIED_STRUCTURE = {
      "task_statuses": [all_models.CycleTaskGroupObjectTask.VERIFIED] * 3,
      "group_status": all_models.CycleTaskGroup.VERIFIED,
      "cycle_status": all_models.Cycle.VERIFIED,
      "workflow_status": all_models.Workflow.INACTIVE,
  }
  ASSIGNED_STRUCTURE = {
      "task_statuses": [all_models.CycleTaskGroupObjectTask.ASSIGNED] * 3,
      "group_status": all_models.CycleTaskGroup.IN_PROGRESS,
      "cycle_status": all_models.Cycle.IN_PROGRESS,
      "workflow_status": all_models.Workflow.ACTIVE
  }
  IN_PROGRESS_STRUCTURE = {
      "task_statuses": [all_models.CycleTaskGroupObjectTask.IN_PROGRESS] * 3,
      "group_status": all_models.CycleTaskGroup.IN_PROGRESS,
      "cycle_status": all_models.Cycle.IN_PROGRESS,
      "workflow_status": all_models.Workflow.ACTIVE
  }
  DECLINED_STRUCTURE = {
      "task_statuses": [all_models.CycleTaskGroupObjectTask.DECLINED] * 3,
      "group_status": all_models.CycleTaskGroup.IN_PROGRESS,
      "cycle_status": all_models.Cycle.IN_PROGRESS,
      "workflow_status": all_models.Workflow.ACTIVE,
  }
  FINISHED_STRUCTURE = {
      "task_statuses": [all_models.CycleTaskGroupObjectTask.FINISHED] * 3,
      "group_status": all_models.CycleTaskGroup.FINISHED,
      "cycle_status": all_models.Cycle.FINISHED,
      "workflow_status": all_models.Workflow.ACTIVE,
  }

  def _update_structure(self, structure=None):
    """Update structure of setuped objects."""
    if not structure:
      return
    structure = structure or {}
    start_statuses = structure.get("task_statuses") or []
    if start_statuses:
      for idx, status in enumerate(start_statuses):
        self.tasks[idx].status = status
    self.group.status = structure.get("group_status", self.group.status)
    self.cycle.status = structure.get("cycle_status", self.cycle.status)
    self.cycle.is_verification_needed = structure.get(
        "cycle_is_verification_needed",
        self.cycle.is_verification_needed)
    self.workflow.status = structure.get("workflow_status",
                                         self.workflow.status)
    db.session.commit()

  def _get_start_tasks_statuses(self, start_structure=None):
    start_statuses = (start_structure or {}).get("task_statuses", [])
    return (start_statuses + self.DEFAULT_TASK_STATUSES)[:3]

  def build_import_data(self, task_statuses):
    return [OrderedDict([("object_type", self.ALIAS),
                         ("Code*", self.tasks[idx].slug),
                         ("State", status)])
            for idx, status in enumerate(task_statuses)]

  @ddt.unpack
  @ddt.data(
      {"update_structure": VERIFIED_STRUCTURE},
      {"update_structure": IN_PROGRESS_STRUCTURE},
      {"update_structure": FINISHED_STRUCTURE},
      # verified few tasks
      {"update_structure": {
          "task_statuses": [all_models.CycleTaskGroupObjectTask.VERIFIED] * 2,
          "group_status": all_models.CycleTaskGroup.IN_PROGRESS,
          "cycle_status": all_models.Cycle.IN_PROGRESS,
          "workflow_status": all_models.Workflow.ACTIVE,
      }},
      {"update_structure": DECLINED_STRUCTURE},
      {"update_structure": VERIFIED_STRUCTURE,
       "start_structure": IN_PROGRESS_STRUCTURE},
      {"update_structure": IN_PROGRESS_STRUCTURE,
       "start_structure": VERIFIED_STRUCTURE},
      {"update_structure": DECLINED_STRUCTURE,
       "start_structure": IN_PROGRESS_STRUCTURE},
      {"update_structure": IN_PROGRESS_STRUCTURE,
       "start_structure": DECLINED_STRUCTURE},
  )
  def test_update_status(self, update_structure, start_structure=None):
    """Simple update task status to {update_structure[task_statuses]}"""
    self._update_structure(start_structure)
    start_statuses = self._get_start_tasks_statuses(start_structure)
    task_count = len(CycleTaskGroupObjectTask.query.all())
    self.assertEqual(start_statuses, [t.status for t in self.tasks])
    task_statuses = update_structure["task_statuses"]
    group_status = update_structure["group_status"]
    cycle_status = update_structure["cycle_status"]
    workflow_status = update_structure["workflow_status"]
    response = self.import_data(*self.build_import_data(task_statuses))
    self._check_csv_response(response, {})
    self.tasks = CycleTaskGroupObjectTask.query.filter(
        CycleTaskGroupObjectTask.id.in_(self.task_ids)
    ).all()
    self.assertEqual(task_statuses + start_statuses[len(task_statuses):],
                     [t.status for t in self.tasks])
    group = self.tasks[0].cycle_task_group
    self.assertEqual(group_status, group.status)
    self.assertEqual(len(CycleTaskGroupObjectTask.query.all()), task_count)
    self.assertEqual(cycle_status, group.cycle.status)
    self.assertEqual(workflow_status, group.cycle.workflow.status)

  @ddt.data(ASSIGNED_STRUCTURE,
            IN_PROGRESS_STRUCTURE,
            DECLINED_STRUCTURE)
  def test_update_to_verified(self, start_structure):
    """Update task status to verified from {0[task_statuses]} and back"""
    self._update_structure(start_structure)
    start_statuses = self._get_start_tasks_statuses(start_structure)
    self.assertEqual(start_statuses, [t.status for t in self.tasks])
    self.assertEqual([None] * len(self.tasks),
                     [t.finished_date for t in self.tasks])
    self.assertEqual([None] * len(self.tasks),
                     [t.verified_date for t in self.tasks])
    task_statuses = self.VERIFIED_STRUCTURE["task_statuses"]
    response = self.import_data(*self.build_import_data(task_statuses))
    self._check_csv_response(response, {})
    self.tasks = CycleTaskGroupObjectTask.query.filter(
        CycleTaskGroupObjectTask.id.in_(self.task_ids)
    ).all()
    self.assertEqual(task_statuses + start_statuses[len(task_statuses):],
                     [t.status for t in self.tasks])
    finished_dates = [t.finished_date for t in self.tasks]
    self.assertNotEqual([None] * len(self.tasks), finished_dates)
    verified_dates = [t.verified_date for t in self.tasks]
    self.assertNotEqual([None] * len(self.tasks), verified_dates)
    self.assertFalse(self.tasks[0].cycle.is_current)
    # wrong rollback  case (try to import from verified to finished)
    response = self.import_data(*self.build_import_data(start_statuses))
    line_error_tmpl_1 = errors.INVALID_STATUS_DATE_CORRELATION.format(
        date="Actual Verified Date",
        status="not Verified",
        line="{}"
    )
    line_error_tmpl_2 = errors.INVALID_STATUS_DATE_CORRELATION.format(
        date="Actual Finish Date",
        status="not Finished",
        line="{}"
    )
    verfied_date_errors = {line_error_tmpl_1.format(i + 3)
                           for i in xrange(len(self.tasks))}
    finished_date_errors = {line_error_tmpl_2.format(i + 3)
                            for i in xrange(len(self.tasks))}
    self._check_csv_response(
        response,
        {
            "Cycle Task": {
                "row_errors": verfied_date_errors | finished_date_errors
            }
        }
    )
    self.tasks = CycleTaskGroupObjectTask.query.filter(
        CycleTaskGroupObjectTask.id.in_(self.task_ids)
    ).all()
    # nothing change
    self.assertEqual(task_statuses + start_statuses[len(task_statuses):],
                     [t.status for t in self.tasks])
    self.assertEqual(finished_dates, [t.finished_date for t in self.tasks])
    self.assertEqual(verified_dates, [t.verified_date for t in self.tasks])
    self.assertFalse(self.tasks[0].cycle.is_current)
    # correct rollback
    rollback_data = self.build_import_data(start_statuses)
    # setup verified dates as empty
    for line in rollback_data:
      line["Actual Verified Date"] = "--"
      line["Actual Finish Date"] = "--"
    response = self.import_data(*rollback_data)
    self._check_csv_response(response, {})
    self.tasks = CycleTaskGroupObjectTask.query.filter(
        CycleTaskGroupObjectTask.id.in_(self.task_ids)
    ).all()
    # assert correct rollback
    self.assertEqual(start_statuses, [t.status for t in self.tasks])
    self.assertEqual([None] * len(self.tasks),
                     [t.finished_date for t in self.tasks])
    self.assertEqual([None] * len(self.tasks),
                     [t.verified_date for t in self.tasks])
    self.assertTrue(self.tasks[0].cycle.is_current)

  @ddt.data(1, 2, 3)
  def test_update_finished_to_verified(self, number_of_tasks):
    """Update {0} tasks status from finished from verified and back"""
    now = datetime.datetime.now().replace(microsecond=0)
    finished_date = now - datetime.timedelta(1)
    start_statuses = self._get_start_tasks_statuses(self.FINISHED_STRUCTURE)
    with ggrc_factories.single_commit():
      for task in self.tasks:
        task.finished_date = finished_date
    self._update_structure(self.FINISHED_STRUCTURE)
    self.tasks = CycleTaskGroupObjectTask.query.filter(
        CycleTaskGroupObjectTask.id.in_(self.task_ids)
    ).all()
    self.assertEqual([finished_date] * len(self.tasks),
                     [t.finished_date for t in self.tasks])
    self.assertEqual([None] * len(self.tasks),
                     [t.verified_date for t in self.tasks])
    task_statuses = [
        all_models.CycleTaskGroupObjectTask.VERIFIED
    ] * number_of_tasks
    response = self.import_data(*self.build_import_data(task_statuses))
    self._check_csv_response(response, {})
    self.tasks = CycleTaskGroupObjectTask.query.filter(
        CycleTaskGroupObjectTask.id.in_(self.task_ids)
    ).all()
    self.assertEqual(task_statuses + start_statuses[len(task_statuses):],
                     [t.status for t in self.tasks])
    self.assertEqual([finished_date] * len(self.tasks),
                     [t.finished_date for t in self.tasks])
    verified_dates = [t.verified_date for t in self.tasks][:number_of_tasks]
    self.assertNotEqual([None] * number_of_tasks, verified_dates)
    verified_dates += [t.verified_date for t in self.tasks][number_of_tasks:]
    self.assertEqual(
        [None] * (len(self.tasks) - number_of_tasks),
        [t.verified_date for t in self.tasks][number_of_tasks:])
    self.assertEqual(len(self.tasks) != number_of_tasks,
                     self.tasks[0].cycle.is_current)
    # wrong rollback  case (try to import from verified to finished)
    response = self.import_data(*self.build_import_data(start_statuses))
    line_error_tmpl = errors.INVALID_STATUS_DATE_CORRELATION.format(
        date="Actual Verified Date",
        status="not Verified",
        line="{}"
    )
    self._check_csv_response(
        response,
        {
            "Cycle Task": {
                "row_errors": {line_error_tmpl.format(idx + 3)
                               for idx in xrange(number_of_tasks)}
            }
        }
    )
    self.tasks = CycleTaskGroupObjectTask.query.filter(
        CycleTaskGroupObjectTask.id.in_(self.task_ids)
    ).all()
    # nothing change
    self.assertEqual(task_statuses + start_statuses[len(task_statuses):],
                     [t.status for t in self.tasks])
    self.assertEqual([finished_date] * len(self.tasks),
                     [t.finished_date for t in self.tasks])
    self.assertEqual(len(self.tasks) != number_of_tasks,
                     self.tasks[0].cycle.is_current)
    self.assertEqual(
        verified_dates,
        [t.verified_date for t in self.tasks])
    # correct rollback
    rollback_data = self.build_import_data(start_statuses)
    # setup verified dates as empty
    for line in rollback_data:
      line["Actual Verified Date"] = "--"
    response = self.import_data(*rollback_data)
    self._check_csv_response(response, {})
    self.tasks = CycleTaskGroupObjectTask.query.filter(
        CycleTaskGroupObjectTask.id.in_(self.task_ids)
    ).all()
    # assert correct rollback
    self.assertEqual(start_statuses, [t.status for t in self.tasks])
    self.assertEqual([finished_date] * len(self.tasks),
                     [t.finished_date for t in self.tasks])
    self.assertEqual([None] * len(self.tasks),
                     [t.verified_date for t in self.tasks])
    self.assertTrue(self.tasks[0].cycle.is_current)

  @staticmethod
  def __build_error_tmpl(error_tmpl, **context):
    """Create simple temaplte from base error tmpl."""
    if "line" not in context:
      context["line"] = "{}"
    return error_tmpl.format(**context)

  def __build_status_error_resp(self, key, error_tmpl, exception_statuses):
    """Return expected response dict based on sent arguments."""
    error_tmpl = self.__build_error_tmpl(error_tmpl,
                                         column_name="State",
                                         message="Invalid state '{}'")
    return {
        self.ALIAS: {
            key: {error_tmpl.format(3 + idx, status)
                  for idx, status in enumerate(exception_statuses)},
        }
    }

  def __assert_error_message(self,
                             sending_data,
                             expected_messages,
                             start_structure=None):
    """Assert validation error message on import cycle task statuses."""
    start_statuses = self._get_start_tasks_statuses(start_structure)

    group_status = self.group.status
    cycle_status = self.cycle.status
    workflow_status = self.workflow.status
    self.assertEqual(start_statuses, [t.status for t in self.tasks])
    response = self.import_data(*sending_data)
    self._check_csv_response(response, expected_messages)
    self.tasks = CycleTaskGroupObjectTask.query.filter(
        CycleTaskGroupObjectTask.id.in_(self.task_ids)
    ).all()
    group = self.tasks[0].cycle_task_group
    self.assertEqual(start_statuses, [t.status for t in self.tasks])
    self.assertEqual(group_status, group.status)
    self.assertEqual(cycle_status, group.cycle.status)
    self.assertEqual(workflow_status, group.cycle.workflow.status)

  @ddt.data(
      VERIFIED_STRUCTURE["task_statuses"],
      DECLINED_STRUCTURE["task_statuses"],
  )
  def test_validation_error(self, exception_statuses):
    """Validation cycle task status update to {0} if no verification needed."""
    self._update_structure({"cycle_is_verification_needed": False})
    error_msgs = self.__build_status_error_resp("row_errors",
                                                errors.VALIDATION_ERROR,
                                                exception_statuses)
    send_data = self.build_import_data(exception_statuses)
    self.__assert_error_message(send_data, error_msgs)

  @ddt.unpack
  @ddt.data(
      {"start_structure": IN_PROGRESS_STRUCTURE,
       "exception_statuses": ["Absolutely Wrong Status"] * 3},
      {"start_structure": IN_PROGRESS_STRUCTURE,
       "exception_statuses": [""] * 3},
      {"exception_statuses": [""] * 3},
      {"exception_statuses": ["Absolutely Wrong Status"] * 3},
      {"start_structure": FINISHED_STRUCTURE,
       "exception_statuses": ["Absolutely Wrong Status"] * 3},
      {"start_structure": FINISHED_STRUCTURE,
       "exception_statuses": [""] * 3},
  )
  def test_simple_send_invalid_status(self,
                                      exception_statuses,
                                      start_structure=None):
    """Validation cycle task status update to {exception_statuses}."""
    self._update_structure(start_structure)
    warn_msgs = self.__build_status_error_resp("row_warnings",
                                               errors.WRONG_VALUE_CURRENT,
                                               exception_statuses)
    send_data = self.build_import_data(exception_statuses)
    self.__assert_error_message(send_data,
                                warn_msgs,
                                start_structure=start_structure)

  @ddt.data(
      ("Actual Finish Date", "Actual Verified Date"),
      ("Start Date", "Due Date"),
  )
  def test_for_date_compare_error(self, columns):
    """Validate task import data where {0[0]} bigger than {0[1]}."""
    self._update_structure(self.VERIFIED_STRUCTURE)
    today = datetime.date.today()
    dates = (today, today - datetime.timedelta(7))
    error_tmpl = self.__build_error_tmpl(errors.INVALID_START_END_DATES,
                                         start_date=columns[0],
                                         end_date=columns[1])
    # line format
    error_resp = {self.ALIAS: {"row_errors": {error_tmpl.format(3)}}}
    data_to_import = OrderedDict([("object_type", self.ALIAS),
                                  ("Code*", self.tasks[0].slug)])
    for column, date in zip(columns, dates):
      data_to_import[column] = date
    response = self.import_data(data_to_import)
    self._check_csv_response(response, error_resp)

  @ddt.data(
      ("Actual Finish Date", "not Finished"),
      ("Actual Verified Date", "not Verified"),
  )
  @ddt.unpack
  def test_for_date_state_error(self, column, status):
    """Validate task {0} not allowed for in {0} tasks."""
    self._update_structure(self.IN_PROGRESS_STRUCTURE)
    today = datetime.date.today()
    error_tmpl = self.__build_error_tmpl(
        errors.INVALID_STATUS_DATE_CORRELATION,
        date=column,
        status=status,
    )
    # line format
    error_resp = {self.ALIAS: {"row_errors": {error_tmpl.format(3)}}}
    data_to_import = OrderedDict([("object_type", self.ALIAS),
                                  ("Code*", self.tasks[0].slug),
                                  (column, today)])
    response = self.import_data(data_to_import)
    self._check_csv_response(response, error_resp)
