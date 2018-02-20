# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""TaskGroup model related tests."""

from ggrc.models import all_models
from ggrc_workflows import ac_roles
from integration.ggrc.models import factories
from integration.ggrc_workflows.helpers import workflow_test_case


class TestTaskGroupApiCalls(workflow_test_case.WorkflowTestCase):
  """Tests related to TaskGroup REST API calls."""

  def test_post_tg_g_editor_admin(self):
    """POST TaskGroup logged in as GlobalEditor & WF Admin."""
    with factories.single_commit():
      self.setup_helper.setup_workflow((self.rbac_helper.GE_RNAME,))

    g_editor = self.setup_helper.get_workflow_person(
        self.rbac_helper.GE_RNAME, ac_roles.workflow.ADMIN_NAME)
    self.api_helper.set_user(g_editor)

    workflow = all_models.Workflow.query.one()

    data = self.api_helper.get_task_group_post_dict(workflow, g_editor)
    response = self.api_helper.post(all_models.TaskGroup, data)
    self.assertEqual(response.status_code, 201)
