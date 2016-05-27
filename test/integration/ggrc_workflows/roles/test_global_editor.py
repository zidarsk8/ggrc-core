# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: brodul@reciprocitylabs.com
# Maintained By: brodul@reciprocitylabs.com
"""
Test if Global Editor role has the permission to access the workflow objects,
owned by Admin.
"""
# TODO: write tests for create, update, delete

from ggrc_workflows.models import Workflow
from ggrc_workflows.models import WorkflowPerson
from ggrc_workflows.models import TaskGroup
from ggrc_workflows.models import TaskGroupObject
from ggrc_workflows.models import TaskGroupTask
from ggrc_workflows.models import Cycle
from ggrc_workflows.models import CycleTaskGroup
from ggrc_workflows.models import CycleTaskGroupObjectTask

from integration.ggrc_workflows.roles import WorkflowRolesTestCase


class GlobalEditorTest(WorkflowRolesTestCase):

  def setUp(self):
    super(GlobalEditorTest, self).setUp()
    self.api.set_user(self.users['editor'])

  def test_get_workflow_objects(self):
    workflow_res = self.api.get(Workflow, self.workflow_obj.id)
    self.assert200(workflow_res)

    task_group_res = self.api.get(TaskGroup, self.first_task_group.id)
    self.assert200(task_group_res)

    task_group_object_res = self.api.get(
        TaskGroupObject, self.first_task_group_object.id)
    self.assert200(task_group_object_res)

    task_group_task_res = self.api.get(
        TaskGroupTask, self.first_task_group_task.id)
    self.assert200(task_group_task_res)

    workflow_person_res = self.api.get(
        WorkflowPerson, self.first_workflow_person.id)
    self.assert200(workflow_person_res)

  def test_get_active_workflow_objects(self):
    self.workflow_res, self.workflow_obj = \
        self.activate_workflow_with_cycle(self.workflow_obj)
    self.get_first_objects()

    workflow_res = self.api.get(Workflow, self.workflow_obj.id)
    self.assert200(workflow_res)

    task_group_res = self.api.get(TaskGroup, self.first_task_group.id)
    self.assert200(task_group_res)

    task_group_object_res = self.api.get(
        TaskGroupObject, self.first_task_group_object.id)
    self.assert200(task_group_object_res)

    task_group_task_res = self.api.get(
        TaskGroupTask, self.first_task_group_task.id)
    self.assert200(task_group_task_res)

    workflow_person_res = self.api.get(
        WorkflowPerson, self.first_workflow_person.id)
    self.assert200(workflow_person_res)

    cycle_obj = self.session.query(Cycle)\
        .filter(Cycle.workflow_id == self.workflow_obj.id)\
        .first()
    cycle_res = self.api.get(
        Cycle, cycle_obj.id)
    self.assert200(cycle_res)

    cycle_task_group_obj = self.session.query(CycleTaskGroup)\
        .filter(CycleTaskGroup.cycle_id == cycle_obj.id)\
        .first()
    cycle_task_group_res = self.api.get(
        CycleTaskGroup, cycle_task_group_obj.id)
    self.assert200(cycle_task_group_res)

    cycle_task_group_object_task_obj =\
        self.session.query(CycleTaskGroupObjectTask)\
        .filter(
            CycleTaskGroupObjectTask.cycle_task_group_id ==
            cycle_task_group_obj.id)\
        .first()
    cycle_task_group_object_task_res = self.api.get(
        CycleTaskGroupObjectTask, cycle_task_group_object_task_obj.id)
    self.assert200(cycle_task_group_object_task_res)
