# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

scope = "Workflow"
description = """
  """
permissions = {
    "read": [
        "Workflow",
        "WorkflowPerson",
        "TaskGroup",
        "TaskGroupObject",
        "TaskGroupTask",
        "Cycle",
        "CycleTaskGroup",
        "CycleTaskGroupObject",
        "CycleTaskGroupObjectTask",
        "CycleTaskEntry",
        "UserRole",
        "Context",
        "Document",
        "ObjectDocument",
        "ObjectFolder",
        "ObjectFile",
    ],
    "create": [
        "WorkflowPerson",
        "CycleTaskEntry",
        "Document",
        "ObjectDocument",
        "ObjectFolder",
        "ObjectFile",
    ],
    "update": [
        "WorkflowPerson",
        "Cycle",
        "CycleTaskGroup",
        "CycleTaskGroupObject",
        "CycleTaskGroupObjectTask",
        "CycleTaskEntry",
        "Document",
        "ObjectDocument",
        "ObjectFolder",
        "ObjectFile",
    ],
    "delete": [
        "WorkflowPerson",
        "CycleTaskEntry",
        "Document",
        "ObjectDocument",
        "ObjectFolder",
        "ObjectFile",
    ],
    "view_object_page": [
        "Workflow",
    ],
}
