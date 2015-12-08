# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

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
        "ObjectPerson",
        "ObjectSection",
        "Relationship"
    ],
    "delete": [
        "ObjectDocument",
        "ObjectPerson",
        "ObjectSection",
        "Relationship",
        "ObjectFolder"
    ]
}
