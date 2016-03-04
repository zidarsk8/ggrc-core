# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

from lib import cache
from lib import exception
from lib import base
from lib import constants
from lib.page.widget import info


def _all_subclasses(cls):
  """Returns all subclassses for a parent"""
  return cls.__subclasses__() + \
         [g for s in cls.__subclasses__() for g in _all_subclasses(s)]


def _factory(cls_name, parent_cls, search_nested_subclasses=False):
  """Returns a subclass from parent
  Args:
    cls_name (basestring)
    parent_cls (cls)
    search_nested_subclasses (bool)
  Returns:
    cls
  """
  cls_name.lower()

  members = _all_subclasses(parent_cls) \
      if search_nested_subclasses \
      else parent_cls.__subclasses__()

  for member_cls in members:
    if member_cls.__name__.lower() == cls_name:
      break
  else:
    raise exception.NoClassFound("%s for parent %s" % (cls_name, parent_cls))

  return member_cls


def get_method_lhn_select(object_name):
  """Returns the method of LHN class
  Args:
    object_name (basestring)
  """
  return constants.method.SELECT_PREFIX + \
         cache.LHN_SECTION_MEMBERS[object_name]


def get_cls_test_utils(object_name):
  """Returns a test utils class based on object name
  Args:
    object_name (basestring)
  """
  # since class names don't allow underscore in names, we're parsing them out
  object_subcls_name = object_name  if "_" not in object_name \
      else object_name.replace("_", "")

  cls_name = constants.cls.TEST_MODAL_NEW_PREFIX + \
             object_subcls_name + \
             constants.cls.TEST_MODAL_NEW_POSTFIX
  return _factory(cls_name, base.Test)


def get_cls_info_widget(object_name):
  """Returns the info widget class
  Args:
      object_name (basestring)
  """
  cls_name = object_name.lower() + constants.cls.INFO_POSTFIX
  return _factory(cls_name, info.InfoWidget)
