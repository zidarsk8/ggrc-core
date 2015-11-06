# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

import unittest
from datetime import date


from ggrc_workflows.models import task_group_task

class TestTaskGroupTask(unittest.TestCase):

  def test_validate_task_type(self):
    t = task_group_task.TaskGroupTask()
    self.assertRaises(ValueError, t.validate_task_type, "task_type", "helloh")
    self.assertEqual("menu", t.validate_task_type("task_type", "menu"))

  def test_validate_date(self):
    t = task_group_task.TaskGroupTask()
    self.assertEqual(date(2002, 4, 16), t.validate_date(date(2,4,16)))

  def test_validate_end_date(self):
    t = task_group_task.TaskGroupTask()
    t.end_date = date(15, 4, 17)
    self.assertEqual(date(2015, 4, 17), t.end_date)

  def test_validate_start_date(self):
    t = task_group_task.TaskGroupTask()
    t.start_date = date(22, 4, 16)
    self.assertEqual(date(2022, 4, 16), t.start_date)
