# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""A module with unit tests for the Task Group model."""

import unittest
from mock import MagicMock, patch

from ggrc_workflows.models import task_group


class TestTaskGroupTask(unittest.TestCase):
  """Consists of Task Group model unittests."""

  def setUp(self):
    """Setup Task Group model tests.
    :return: None
    """
    task_group.db = MagicMock()

  # pylint: disable=invalid-name
  def test_copy_when_clone_people_is_true_and_contact_is_not_none(self):
    """ Test copy() method with next parameters:
    clone_people: True
    self.contact: not None
    :return: None
    """
    taskgroup = task_group.TaskGroup()
    taskgroup.contact = 'Person id=0x0000AABBCCDDEEFF'
    result = taskgroup.copy(clone_people=True)
    self.assertEqual(result.contact, taskgroup.contact)

  @patch("ggrc_workflows.models.task_group.get_current_user",
         return_value="Current user person id=0x0011223344556677")
  # pylint: disable=invalid-name
  def test_copy_when_clone_people_is_false_and_contact_is_not_none(
      self, get_current_user,
  ):
    """ Test copy() method with next parameters:
        clone_people: False
        self.contact: not None
        :return: None
        """
    taskgroup = task_group.TaskGroup()
    taskgroup.contact = 'Person id=0x0000AABBCCDDEEFF'
    result = taskgroup.copy(clone_people=False)
    self.assertEqual(result.contact, get_current_user())

  @patch("ggrc_workflows.models.task_group.get_current_user",
         return_value="Current user person id=0x0011223344556677")
  # pylint: disable=invalid-name
  def test_copy_when_clone_people_is_true_and_contact_is_none(
      self, get_current_user
  ):
    """ Test copy() method with next parameters:
        clone_people: True
        self.contact: None
        :return: None
        """
    taskgroup = task_group.TaskGroup()
    taskgroup.contact = None
    result = taskgroup.copy(clone_people=True)
    self.assertEqual(result.contact, get_current_user())

  @patch("ggrc_workflows.models.task_group.get_current_user",
         return_value="Current user person id=0x0011223344556677")
  # pylint: disable=invalid-name
  def test_copy_when_clone_people_is_false_and_contact_is_none(
      self, get_current_user
  ):
    """ Test copy() method with next parameters:
        clone_people: False
        self.contact: None
        :return: None
        """
    taskgroup = task_group.TaskGroup()
    taskgroup.contact = None
    result = taskgroup.copy(clone_people=False)
    self.assertEqual(result.contact, get_current_user())
