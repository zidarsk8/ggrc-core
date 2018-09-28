# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Factories for app_entity."""
from lib import users
from lib.entities import app_entity
from lib.utils import random_utils


class _BaseFactory(object):
  """Base factory for app entities."""

  @property
  def _entity_cls(self):
    """Returns an app entity to create. To be overridden in subclass."""
    raise NotImplementedError

  @property
  def _random_attrs(self):
    """Returns a dict with additional default arguments to pass to app entity's
    constructor. To be overridden in subclass.
    """
    raise NotImplementedError

  def create(self, **attrs):
    """Creates a random app entity with `args`."""
    attrs.update(self._random_attrs)
    return self.create_empty(**attrs)

  def create_empty(self, **attrs):
    """Creates an app entity from `args`. Attributes that are not passed,
    will be set to None.
    """
    attr_names = self._entity_cls.fields()
    all_attrs = dict.fromkeys(attr_names)
    for attr_name, attr_value in attrs.iteritems():
      all_attrs[attr_name] = attr_value
    return self._entity_cls(**all_attrs)

  @property
  def _obj_title(self):
    """Returns a random object title for the object."""
    return random_utils.get_title(self._obj_name())

  @classmethod
  def _obj_name(cls):
    """Returns object name for app entity."""
    return cls.__name__.rstrip("Factory")


class WorkflowFactory(_BaseFactory):
  """Factory for Workflow entities."""
  _entity_cls = app_entity.Workflow

  @property
  def _random_attrs(self):
    """See superclass."""
    return {
        "title": self._obj_title,
        "admins": [users.current_person()],
        "wf_members": [],
        "task_groups": []
    }


class TaskGroupFactory(_BaseFactory):
  """Factory for TaskGroup entities."""
  _entity_cls = app_entity.TaskGroup

  @property
  def _random_attrs(self):
    """See superclass."""
    return {
        "title": self._obj_title,
        "assignee": users.current_person()
    }


class TaskGroupTaskFactory(_BaseFactory):
  """Factory for TaskGroupTask entities."""
  _entity_cls = app_entity.TaskGroupTask

  @property
  def _random_attrs(self):
    """See superclass."""
    return {
        "title": self._obj_title,
        "assignees": [users.current_person()]
    }


class PersonFactory(_BaseFactory):
  """Factory for Person entities."""
  _entity_cls = app_entity.Person

  @property
  def _random_attrs(self):
    """See superclass."""
    return {
        "name": self._obj_title,
        "email": random_utils.get_email()
    }
