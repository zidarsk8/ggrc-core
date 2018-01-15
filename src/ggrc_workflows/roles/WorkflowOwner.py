# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""A module with permissions json for Workflow Owner."""

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
    ],
    "create": [
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
        "Document",
    ],
    "update": [
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
        "Document",
    ],
    "delete": [
        "Workflow",
        "WorkflowPerson",
        "TaskGroup",
        "TaskGroupObject",
        "TaskGroupTask",
        "Cycle",
        "CycleTaskGroup",
        "CycleTaskGroupObject",
        {
            "type": "CycleTaskGroupObjectTask",
            "terms": {
                "property_name": "cycle.is_current",
                "value": True
            },
            "condition": "is"
        },
        "CycleTaskEntry",
        "UserRole",
        "Document",
    ],
    "view_object_page": [
        "Workflow",
    ],
}
