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
