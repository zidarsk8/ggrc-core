# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

""" Module for all special column handlers for workflow objects """

from ggrc.converters.handlers import ColumnHandler
from ggrc.converters.handlers import CheckboxColumnHandler
from ggrc.converters import errors
from ggrc_workflows.models import Workflow
from ggrc_workflows.models import TaskGroup


class FrequencyColumnHandler(ColumnHandler):

  """ Handler for workflow frequency column """

  frequency_map = {
      "one time": "one_time"
  }

  def parse_item(self):
    """ parse frequency value

    Returning None will set the default frequency to one_time.
    """
    if not self.raw_value:
      return None
    value = self.raw_value.lower()
    frequency = self.frequency_map.get(value, value)
    if frequency not in self.row_converter.object_class.VALID_FREQUENCIES:
      self.add_error(errors.WRONG_VALUE, column_name=self.display_name)
    return frequency

  def get_value(self):
    reverse_map = {v: k for k, v in self.frequency_map.items()}
    value = getattr(self.row_converter.obj, self.key, self.value)
    return reverse_map.get(value, value)


class ParentColumnHandler(ColumnHandler):

  """ handler for directly mapped columns """

  parent = None

  def __init__(self, row_converter, key, **options):
    super(ParentColumnHandler, self).__init__(row_converter, key, **options)

  def parse_item(self):
    """ get parent workflow id """
    if self.raw_value == "":
      self.add_error(errors.MISSING_VALUE_ERROR, column_name=self.display_name)
      return None
    slug = self.raw_value
    obj = self.new_objects.get(self.parent, {}).get(slug)
    if obj is None:
      obj = self.parent.query.filter(self.parent.slug == slug).first()
    if obj is None:
      self.add_error(errors.UNKNOWN_OBJECT,
                     object_type=self.parent._inflector.human_singular.title(),
                     slug=slug)
    return obj

  def get_value(self):
    return self.value.slug


class WorkflowColumnHandler(ParentColumnHandler):

  def __init__(self, row_converter, key, **options):
    self.parent = Workflow
    super(WorkflowColumnHandler, self).__init__(row_converter, key, **options)


class TaskGroupColumnHandler(ParentColumnHandler):

  def __init__(self, row_converter, key, **options):
    self.parent = TaskGroup
    super(TaskGroupColumnHandler, self).__init__(row_converter, key, **options)

class TaskDateColumnHandler(ColumnHandler):
  def __init__(self, row_converter, key, **options):
    self.parent = Workflow
    super(TaskDateColumnHandler, self).__init__(row_converter, key, **options)
  pass


class TaskStartColumnHandler(TaskDateColumnHandler):
  pass

class TaskEndColumnHandler(TaskDateColumnHandler):
  pass

COLUMN_HANDLERS = {
    "frequency": FrequencyColumnHandler,
    "workflow": WorkflowColumnHandler,
    "task_group": TaskGroupColumnHandler,
    "notify_on_change": CheckboxColumnHandler,
    "relative_start_date": TaskStartColumnHandler,
    "relative_end_date": TaskEndColumnHandler,
}
