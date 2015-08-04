# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

scope = "Admin"
description = """
  gGRC System Administrator with super-user privileges.
  """
permissions = {
    "read": [],
    "create": [],
    "delete": [],
    "__GGRC_ADMIN__": [
        "__GGRC_ALL__"
    ],
    "update": []
}
