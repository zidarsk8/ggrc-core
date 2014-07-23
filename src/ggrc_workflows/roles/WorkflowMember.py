scope = "Workflow"
description = """
  """
permissions = {
    "read": [
        "Workflow",
        "WorkflowObject",
        "WorkflowPerson",
        "WorkflowTask",
        "Task",
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
    ],
    "create": [
        "WorkflowObject",
        "WorkflowPerson",
        "WorkflowTask",
        "Task",
        "CycleTaskEntry",
    ],
    "update": [
        "WorkflowObject",
        "WorkflowPerson",
        "WorkflowTask",
        "Task",
        "CycleTaskGroupObjectTask",
        "CycleTaskEntry",
    ],
    "delete": [
        "WorkflowObject",
        "WorkflowPerson",
        "WorkflowTask",
        "Task",
        "CycleTaskEntry",
    ],
    "view_object_page": [
        "Workflow",
        "Task",
    ],
}
