# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Task Group info panel."""
from lib import base
from lib.page.widget import table_with_headers


class TaskGroupInfoPanel(base.WithBrowser):
  """Represents Task Group info panel on Workflow Setup tab."""

  def __init__(self):
    super(TaskGroupInfoPanel, self).__init__()
    self._root = self._browser
    self._table = table_with_headers.TableWithHeaders(
        self._root,
        header_locator={"class_name": "task_group_tasks__header-item"},
        table_rows=self.task_rows
    )

  def task_rows(self):
    """Returns task rows."""
    return [TaskRow(row, self._table.table_header_names())
            for row in self._root.elements(class_name="object-list__item")]

  def click_create_task(self):
    """Clicks Create Task button."""
    self._root.link(text="Create Task").click()


class TaskRow(object):
  """Represents task row in info panel."""

  def __init__(self, row_el, header_names):
    self._table_row = table_with_headers.TableRow(
        container=row_el,
        table_header_names=header_names,
        cell_locator={"class_name": "task_group_tasks__list-item-column"},
        header_attr_mapping={"Task Assignees": "assignees"}
    )

  def assignees(self):
    """Returns list of assignees."""
    return [el.text for el in self._table_row.cell_for_header(
        "Task Assignees").elements(class_name="tree-field__item")]

  def start_date(self):
    """Returns start date."""
    return self._initial_setup().split(" - ")[0].strip()

  def due_date(self):
    """Returns due date."""
    return self._initial_setup().split(" - ")[1].strip()

  def obj_dict(self):
    """Returns object dictionary for the row."""
    obj_dict = self._table_row.obj_dict(self)
    obj_dict.update(start_date=self.start_date(), due_date=self.due_date())
    return obj_dict

  def _initial_setup(self):
    """Returns text of initial setup cell."""
    return self._table_row.text_for_header("Initial Setup")
