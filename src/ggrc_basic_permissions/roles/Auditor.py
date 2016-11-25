# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

scope = "Audit"
description = """
  The permissions required by an auditor to access relevant resources for the
  program being audited.
  """
permissions = {
    "read": [
        "Audit",
        "Request",
        "Assessment",
        "Issue",
        "Meeting",
        "ObjectDocument",
        "ObjectPerson",
        "Relationship",
        "Document",
        "Meeting",
        "UserRole",
        "Comment",
        "Context",
    ],
    "create": [
        "Request",
        "Assessment",
        "Issue",
        "Relationship",
        "Comment",
    ],
    "view_object_page": [
        "__GGRC_ALL__"
    ],
    "update": [
        "Request",
        "Assessment",
        "Issue",
        "Audit",
    ],
    "delete": [
        "Request",
        "Assessment",
        "Issue"
    ],
}
