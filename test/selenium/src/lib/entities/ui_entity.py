# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""UI entities."""
# pylint: disable=too-few-public-methods

import attr

from lib.entities import entity_operations


def get_cls_for(obj_type):
  """Returns ui entity for `obj_type`"""
  return {
      "workflow": Workflow
  }[obj_type]


@attr.s
class _Base(object):
  """Represents UI entity."""
  obj_id = attr.ib()

  @classmethod
  def obj_type(cls):
    """Returns object type."""
    return entity_operations.obj_type(cls)


@attr.s
class Workflow(_Base):
  """Represents Workflow on UI."""
  title = attr.ib()
  status = attr.ib()
  description = attr.ib()
  admins = attr.ib()
  workflow_members = attr.ib()
  code = attr.ib()
  created_at = attr.ib()
  updated_at = attr.ib()
  modified_by = attr.ib()
