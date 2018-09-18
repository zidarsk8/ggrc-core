# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Workflow UI facade."""
from lib import factory
from lib.entities import entity_operations, ui_entity, convert
from lib.page.widget import object_page, object_modal
from lib.utils import selenium_utils


def submit_obj(obj):
  """Submits obj. Sets object id and code after that."""
  obj_type = obj.obj_type()
  object_modal.get_modal_obj(obj_type).submit_obj(obj)
  obj.obj_id = object_page.ObjectPage().get_obj_id()
  obj.code = entity_operations.obj_code(
      object_type=obj_type, obj_id=obj.obj_id)


def build_obj(app_obj):
  """Builds the object from the page and returns it."""
  ui_entity_cls = ui_entity.get_cls_for(app_obj.obj_type())
  obj_scope = info_widget_cls(app_obj).obj_scope()
  ui_obj = ui_entity_cls(**obj_scope)
  return convert.ui_to_app(ui_obj)


def info_widget_cls(obj):
  """Returns a corresponding page object from info_widget module."""
  return factory.get_cls_widget(object_name=obj.obj_type(), is_info=True)()


def open_obj_tab_url(obj, obj_tab):
  """Returns an url to the `obj_tab` of `obj`."""
  tab_hash = {
      "Setup": "task_group"
  }[obj_tab]
  obj_url = entity_operations.obj_url(obj)
  selenium_utils.open_url("{}#!{}".format(obj_url, tab_hash))
