# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""App entities.
Design notes:
* Attributes may not be fully set. Value set to None means that
an attribute value is unknown.
It should not be compared when comparing objects.
* If an attribute appears only at one layer (REST, UI or Import), it should
still be here.
"""
import collections

import attr

from lib.entities import entity_operations


@attr.s
class _Base(object):
  """Represents entity."""
  obj_id = attr.ib()

  @classmethod
  def obj_type(cls):
    """Returns object type."""
    return entity_operations.obj_type(cls)

  def obj_dict(self):
    """Returns a dict of attributes."""
    return attr.asdict(self, dict_factory=collections.OrderedDict)


@attr.s
class Workflow(_Base):
  """Represents Workflow entity."""
  title = attr.ib()
  admins = attr.ib()
  wf_members = attr.ib()
  repeat_wf = attr.ib()
  first_task_group_title = attr.ib()
  code = attr.ib()


@attr.s
class Person(_Base):
  """Represents Person entity."""
  email = attr.ib()
