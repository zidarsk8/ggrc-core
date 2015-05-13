scope = "Private Program Implied"
description = """
  A user with authorization to edit mapping objects related to a program. When
  a person has this role they can map and unmap objects to the Program but they
  are unable ble to edit the Program info, delete the Program, or assign roles
  for that Program.
  """
permissions = {
    "read": [
        "ObjectDocument",
        "ObjectObjective",
        "ObjectPerson",
        "ObjectSection",
        "Program",
        "Relationship",
        "ObjectFolder",
        "UserRole",
        "Context",
    ],
    "create": [
        "ObjectDocument",
        "ObjectObjective",
        "ObjectPerson",
        "ObjectSection",
        "Relationship",
        "ObjectFolder"
    ],
    "view_object_page": [
        "__GGRC_ALL__"
    ],
    "update": [
        "ObjectDocument",
        "ObjectObjective",
        "ObjectPerson",
        "ObjectSection",
        "Relationship"
    ],
    "delete": [
        "ObjectDocument",
        "ObjectObjective",
        "ObjectPerson",
        "ObjectSection",
        "Relationship",
        "ObjectFolder"
    ]
}
