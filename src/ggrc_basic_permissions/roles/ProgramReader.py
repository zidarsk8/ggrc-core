# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

scope = "Private Program"
description = """
  A user with authorization to read mapping objects related to an access
  controlled Program.<br/><br/>This is essentially a view only role. A person
  with this role can access and view an otherwise private program, but they
  cannot map to or edit that program in any way.
  """
permissions = {
    "read": [
        "ObjectDocument",
        "ObjectObjective",
        "ObjectPerson",
        "ObjectSection",
        "Program",
        "ProgramDirective",
        "Relationship",
        "UserRole",
        "Context",
    ],
    "create": [],
    "view_object_page": [
        "__GGRC_ALL__"
    ],
    "update": [],
    "delete": []
}
