# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""TaskGroupTask model related tests."""

from ggrc.models import all_models
from ggrc_workflows import ac_roles
from integration.ggrc.models import factories
from integration.ggrc_workflows.helpers import workflow_test_case
from integration.ggrc_workflows.models import factories as wf_factories


class TestTaskApiCalls(workflow_test_case.WorkflowTestCase):
  """Tests related to TaskGroupTask REST API calls."""

  def test_create_task_g_editor_admin(self):
    """POST TaskGroupTask logged in as GlobalEditor & WF Admin."""
    with factories.single_commit():
      workflow = self.setup_helper.setup_workflow((self.rbac_helper.GE_RNAME,))
      wf_factories.TaskGroupFactory(workflow=workflow)

    g_editor = self.setup_helper.get_workflow_person(
        self.rbac_helper.GE_RNAME, ac_roles.workflow.ADMIN_NAME)
    self.api_helper.set_user(g_editor)

    task_group = all_models.TaskGroup.query.one()
    people_roles = {ac_roles.task.ASSIGNEE_NAME: g_editor}

    data = self.api_helper.get_task_post_dict(
        task_group, people_roles, "2018-01-01", "2018-01-02")
    response = self.api_helper.post(all_models.TaskGroupTask, data)
    self.assertEqual(response.status_code, 201)
