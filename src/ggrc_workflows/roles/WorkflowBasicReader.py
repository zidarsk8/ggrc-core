scope = "Workflow Implied"
description = """
  Allow any user assigned a role in a workflow the ability to read basic
  public-context resources.
  """
permissions = {
    "read": [
        "Category",
        "ControlCategory",
        "ControlAssertion",
        "Option",
        "Role",
        "Person",
        "Context",
        {
            "type": "BackgroundTask",
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
