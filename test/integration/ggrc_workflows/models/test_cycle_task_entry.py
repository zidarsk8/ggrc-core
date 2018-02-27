# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""CycleTaskEntry model related tests."""

from ggrc.models import all_models
from ggrc_workflows import ac_roles
from integration.ggrc.models import factories
from integration.ggrc_workflows.helpers import workflow_test_case
from integration.ggrc_workflows.models import factories as wf_factories


class TestCommentApiCalls(workflow_test_case.WorkflowTestCase):
  """Tests related to CycleTaskEntry REST API calls."""

  def test_post_comment_editor_admin(self):
    """POST CycleTaskEntry logged in as GlobalEditor & WF Admin."""
    with factories.single_commit():
      workflow = self.setup_helper.setup_workflow((self.rbac_helper.GE_RNAME,))
      cycle = wf_factories.CycleFactory(workflow=workflow)
      wf_factories.CycleTaskFactory(cycle=cycle)

    g_editor = self.setup_helper.get_workflow_person(
        self.rbac_helper.GE_RNAME, ac_roles.workflow.ADMIN_NAME)
    self.api_helper.set_user(g_editor)

    cycle_task = all_models.CycleTaskGroupObjectTask.query.one()

    data = self.api_helper.get_cycle_task_entry_post_dict(cycle_task)
    response = self.api_helper.post(all_models.CycleTaskEntry, data)
    self.assertEqual(response.status_code, 201)
