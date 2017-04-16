# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Handlers for access control roles."""

from ggrc import models
from ggrc.converters.handlers import handlers


class AccessControlRoleColumnHandler(handlers.UsersColumnHandler):
  """Handler for access control roles."""

  def set_obj_attr(self):
    role = models.AccessControlRole.query.filter_by(
        name=self.display_name).one()
    for person in self.value:
      models.AccessControlList(
          object=self.row_converter.obj,
          person=person,
          ac_role_id=role.id
      )
