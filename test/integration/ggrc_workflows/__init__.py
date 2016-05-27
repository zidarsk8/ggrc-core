# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com
from integration.ggrc import TestCase
from integration.ggrc_workflows.generator import WorkflowsGenerator
from integration.ggrc.api_helper import Api
from integration.ggrc.generator import ObjectGenerator


class WorkflowTestCase(TestCase):

  def setUp(self):
    super(WorkflowTestCase, self).setUp()
    self.api = Api()
    self.generator = WorkflowsGenerator()
    self.object_generator = ObjectGenerator()

    self.random_objects = self.object_generator.generate_random_objects()
