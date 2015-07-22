# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

""" Module for all special column handlers for workflow objects """

from datetime import date

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
      self.add_error(errors.WRONG_VALUE_ERROR, column_name=self.display_name)
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
    # pylint: disable=protected-access
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

  """ handler for workflow column in task groups """

  def __init__(self, row_converter, key, **options):
    """ init workflow handler """
    self.parent = Workflow
    super(WorkflowColumnHandler, self).__init__(row_converter, key, **options)


class TaskGroupColumnHandler(ParentColumnHandler):

  """ handler for task group column in task group tasks """

  def __init__(self, row_converter, key, **options):
    """ init task group handler """
    self.parent = TaskGroup
    super(TaskGroupColumnHandler, self).__init__(row_converter, key, **options)


class TaskDateColumnHandler(ColumnHandler):

  """ handler for start and end columns in task group tasks """

  def parse_item(self):
    """ parse start and end columns fow workflow tasks

    Parsed item will be in d, m, y order, with possible missisg y.
    """
    try:
      value = [int(v) for v in self.raw_value.split("/")]
      if len(value) > 1:
        tmp = value[0]
        value[0] = value[1]
        value[1] = tmp
      else:
        value.append(0)
      return value
    except ValueError:
      self.add_error(errors.WRONG_VALUE_ERROR, column_name=self.display_name)
    return None


class TaskStartColumnHandler(TaskDateColumnHandler):

  """ handler for start column in task group tasks """

  def set_obj_attr(self):
    """ set all possible start date attributes """
    frequency = self.row_converter.obj.task_group.workflow.frequency
    if frequency == "one_time":
      self.row_converter.obj.start_date = date(*self.value[::-1])
    self.row_converter.obj.relative_start_day = self.value[0]
    self.row_converter.obj.relative_start_month = self.value[1]


class TaskEndColumnHandler(TaskDateColumnHandler):

  """ handler for end column in task group tasks """

  def set_obj_attr(self):
    """ set all possible end date attributes """
    frequency = self.row_converter.obj.task_group.workflow.frequency
    if self.value is None:
      return
    frequency = self.row_converter.obj.task_group.workflow.frequency
    if frequency == "one_time":
      if len(self.value) != 3:
        self.add_error(errors.WRONG_VALUE_ERROR, column_name=self.display_name)
      self.row_converter.obj.end_date = date(*self.value[::-1])
    self.row_converter.obj.relative_end_day = self.value[0]
    self.row_converter.obj.relative_end_month = self.value[1]


class TaskTypeColumnHandler(ColumnHandler):

  """ handler for task type column in task group tasks """

  type_map = {
      "rich text": "text",
      "drop down": "menu",
      "checkboxes": "checkbox",
  }

  def parse_item(self):
    """ parse task type column value """
    if self.raw_value == "":
      return None
    value = self.type_map.get(self.raw_value.lower())
    if value is None:
      self.add_warning(errors.WRONG_REQUIRED_VALUE,
                       value=self.raw_value,
                       column_name=self.display_name)
      value = self.row_converter.obj.default_task_type()
    return value


COLUMN_HANDLERS = {
    "frequency": FrequencyColumnHandler,
    "workflow": WorkflowColumnHandler,
    "task_group": TaskGroupColumnHandler,
    "notify_on_change": CheckboxColumnHandler,
    "relative_start_date": TaskStartColumnHandler,
    "relative_end_date": TaskEndColumnHandler,
    "task_type": TaskTypeColumnHandler,
}
