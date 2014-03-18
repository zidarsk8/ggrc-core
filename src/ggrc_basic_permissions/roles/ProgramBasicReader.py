scope = "Program Implied"
description = """
  Allow any user assigned a role in a program the ability to read Role
  resources.
  """
permissions = {
    "read": [
        "Role",
        "Person",
        {
            "type": "Task",
            "terms": {
                "property_name": "modified_by",
                "value": "$current_user"
            },
            "condition": "is"
        },
    ],
    "create": [],
    "update": [],
    "delete": []
}
