# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for Workflow model."""

from ggrc import db
from ggrc_workflows.models import Workflow
from integration.ggrc import TestCase
from integration.ggrc_workflows.models import factories


class TestWorkflow(TestCase):
  """Tests for Workflow model inner logic"""

  def test_basic_workflow_creation(self):
    """Test basic WF"""
    workflow = factories.WorkflowFactory(title="This is a test WF")
    workflow = db.session.query(Workflow).get(workflow.id)
    self.assertEqual(workflow.title, "This is a test WF")
