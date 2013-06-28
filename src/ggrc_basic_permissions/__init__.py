# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

from flask import session
from ggrc import db
from ggrc.rbac.permissions_provider import DefaultUserPermissions
from ggrc.services.registry import service
from .models import Role, RolePermission, UserRole

class CompletePermissionsProvider(object):
  def __init__(self, settings):
    pass

  def permissions_for(self, user):
    if 'permissions' not in session:
      self.add_permissions_to_session(user)
    return DefaultUserPermissions()

  def add_permissions_to_session(self, user):
    permissions = db.session.query(RolePermission)\
        .join(UserRole.user_id==user.id)
    d = {}
    for p in permissions:
      d.get(p.permission, {}).get(p.resource_type, []).append(p.context_id)
    session['permissions'] = d

def all_collections():
  """The list of all collections provided by this extension."""
  return [
      service('roles', Role),
      service('roles_permissions', RolePermission),
      service('roles_users', UserRole),
      ]
