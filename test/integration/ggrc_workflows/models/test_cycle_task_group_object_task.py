# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module for integration tests for CycleTaskGroupObjectTask specifics."""

import ddt

from ggrc.models import all_models
from integration.ggrc import TestCase as BaseTestCase
from integration.ggrc import api_helper
from integration.ggrc.models import factories
from integration.ggrc_basic_permissions.models import factories as bp_factories
from integration.ggrc_workflows import generator as wf_generator
from integration.ggrc_workflows.models import factories as wf_factories


@ddt.ddt
class TestCTGOT(BaseTestCase):
  """Test suite for CycleTaskGroupObjectTask specific logic."""

  NOBODY = "nobody@example.com"
  WORKFLOW_OWNER = "wfo@example.com"
  TASK_ASSIGNEE_1 = "assignee_1@example.com"
  TASK_ASSIGNEE_2 = "assignee_2@example.com"

  def setUp(self):
    super(TestCTGOT, self).setUp()

    self.api = api_helper.Api()

    with factories.single_commit():
      assignee_1 = factories.PersonFactory(email=self.TASK_ASSIGNEE_1)
      assignee_2 = factories.PersonFactory(email=self.TASK_ASSIGNEE_2)
      workflow_owner = factories.PersonFactory(email=self.WORKFLOW_OWNER)
      nobody = factories.PersonFactory(email=self.NOBODY)

      workflow_owner_role = (all_models.Role.query
                             .filter_by(name="WorkflowOwner").one())
      reader_role = all_models.Role.query.filter_by(name="Reader").one()
      for person in [assignee_1, assignee_2, workflow_owner, nobody]:
        bp_factories.UserRoleFactory(person=person,
                                     role=reader_role,
                                     context=None)

      workflow = wf_factories.WorkflowFactory()
      taskgroup = wf_factories.TaskGroupFactory(workflow=workflow)
      wf_factories.TaskGroupTaskFactory(task_group=taskgroup,
                                        contact=assignee_1)
      wf_factories.TaskGroupTaskFactory(task_group=taskgroup,
                                        contact=assignee_2)
      bp_factories.UserRoleFactory(person=workflow_owner,
                                   role=workflow_owner_role,
                                   context=workflow.context)

    generator = wf_generator.WorkflowsGenerator()
    generator.generate_cycle(workflow)
    generator.activate_workflow(workflow)

  @ddt.data((NOBODY, [False, False]),
            (WORKFLOW_OWNER, [True, True]),
            (TASK_ASSIGNEE_1, [True, False]),
            (TASK_ASSIGNEE_2, [False, True]))
  @ddt.unpack
  def test_allow_change_state(self, user, expected_values):
    user = all_models.Person.query.filter_by(email=user).one()
    self.api.set_user(user)
    response = self.api.get_query(all_models.CycleTaskGroupObjectTask,
                                  "__sort=id")
    self.assert200(response)

    cycle_tasks = (response.json
                           .get("cycle_task_group_object_tasks_collection", {})
                           .get("cycle_task_group_object_tasks", []))
    # relies on same order of ids of TGT and CTGOT
    self.assertListEqual(
        [cycle_task["allow_change_state"] for cycle_task in cycle_tasks],
        expected_values,
    )
