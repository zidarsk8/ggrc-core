# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""TaskGroupObject model related tests."""

from ggrc.models import all_models
from ggrc_workflows import ac_roles
from integration.ggrc.models import factories
from integration.ggrc_workflows.helpers import workflow_test_case
from integration.ggrc_workflows.models import factories as wf_factories


class TestTaskGroupObjectApiCalls(workflow_test_case.WorkflowTestCase):
  """Tests related to TaskGroupObject REST API calls."""

  def test_map_obj_to_tg_editor_admin(self):
    """Map Control to TaskGroup logged in as GlobalEditor & Admin."""
    with factories.single_commit():
      workflow = self.setup_helper.setup_workflow((self.rbac_helper.GE_RNAME,))
      wf_factories.TaskGroupFactory(workflow=workflow)
      factories.ControlFactory(directive=None)

    g_editor = self.setup_helper.get_workflow_person(
        self.rbac_helper.GE_RNAME, ac_roles.workflow.ADMIN_NAME)
    self.api_helper.set_user(g_editor)

    task_group = all_models.TaskGroup.query.one()
    control = all_models.Control.query.one()

    data = self.api_helper.get_task_group_object_post_dict(task_group, control)
    response = self.api_helper.post(all_models.TaskGroupObject, data)
    self.assertEqual(response.status_code, 201)
