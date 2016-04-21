# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

from lib import cache
from lib import exception
from lib import base
from lib import constants
from lib.page.widget import info_widget
from lib.page.widget import admin_widget
from lib.page.widget import generic_widget


def _filter_out_underscore(object_name):
  """Since class names don't allow underscore in names, we're parsing them
  out"""
  return object_name if "_" not in object_name \
      else object_name.replace("_", "")


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
  subcls_name = _filter_out_underscore(cls_name.lower())
  members = _all_subclasses(parent_cls) \
      if search_nested_subclasses \
      else parent_cls.__subclasses__()

  for member_cls in members:
    if member_cls.__name__.lower() == subcls_name:
      break
  else:
    raise exception.NoClassFound(
        "%s for parent %s" % (subcls_name, parent_cls))

  return member_cls


def get_method_lhn_select(object_name):
  """Returns the method of LHN class
  Args:
    object_name (basestring)
  """
  return constants.method.SELECT_PREFIX \
      + cache.LHN_SECTION_MEMBERS[object_name]


def get_method_select(object_name):
  """Returns the method of LHN class
  Args:
    object_name (basestring)
  """
  return constants.method.SELECT_PREFIX + object_name


def get_cls_test_utils(object_name):
  """Returns a test utils class based on object name
  Args:
    object_name (basestring)
  """
  cls_name = constants.cls_name.TEST_MODAL_NEW_PREFIX + object_name
  return _factory(cls_name, base.TestUtil, search_nested_subclasses=True)


def get_cls_widget(object_name, is_info=False, is_admin=False):
  """Returns the info widget class
  Args:
      object_name (basestring)
  """
  if is_info:
    base_cls = info_widget.Widget
  elif is_admin:
    base_cls = admin_widget.Widget
  else:
    base_cls = generic_widget.Widget
  return _factory(object_name, base_cls)


def get_locator_widget(widget_name):
  """Returns the locator for the widget tab in the widget bar"""
  # todo: unittests
  return getattr(constants.locator.WidgetBar, widget_name.upper())


def get_locator_add_widget(widget_name):
  """Returns the locator for the selected widget from the add widget button
  dropdown in the widget bar"""
  # todo: unittests
  return getattr(
      constants.locator.WidgetBarButtonAddDropdown, widget_name.upper())
