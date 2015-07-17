# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

scope = "Private Program Implied"
description = """
  A user with Auditor role for a program audit will also have this role in the
  program context so that the auditor will have access to the private program
  information and mappings required to perform the audit.
  """
permissions = {
    "read": [
        "ObjectDocument",
        "ObjectPerson",
        "Program",
        "Relationship",
        "Context",
        "UserRole"
    ],
    "create": [],
    "update": [],
    "delete": []
}
