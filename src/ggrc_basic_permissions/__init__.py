# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

from flask import session
from ggrc import db, settings
from ggrc.models.context import Context
from ggrc.rbac.permissions_provider import DefaultUserPermissions
from ggrc.services.registry import service
from .models import Role, UserRole

class CompletePermissionsProvider(object):
  def __init__(self, settings):
    pass

  def permissions_for(self, user):
    if 'permissions' not in session:
      self.add_permissions_to_session(user)
    return DefaultUserPermissions()

  def handle_admin_user(self, user):
    pass

  def add_permissions_to_session(self, user):
    if user is not None \
        and hasattr(settings, 'BOOTSTRAP_ADMIN_USERS') \
        and user.email in settings.BOOTSTRAP_ADMIN_USERS:
      permissions = {
          DefaultUserPermissions.ADMIN_PERMISSION.action: {
            DefaultUserPermissions.ADMIN_PERMISSION.resource_type: [
              DefaultUserPermissions.ADMIN_PERMISSION.context_id,
              ],
            },
          }
    elif user is not None:
      permissions = {}
      user_roles = db.session.query(UserRole).filter(
          UserRole.user_email==user.email).all()
      for user_role in user_roles:
        for action, resource_types in user_role.role.permissions.items():
          for resource_type in resource_types:
            permissions.setdefault(action, {}).setdefault(resource_type, [])\
                .append(user_role.target_context_id)
      #grab personal context
      personal_context = db.session.query(Context).filter(
          Context.related_object_id == user.id,
          Context.related_object_type == 'Person',
          ).first()
      if not personal_context:
        personal_context = Context(
            name='Personal Context for {0}'.format(user.id),
            description='',
            context_id=1,
            related_object_id=user.id,
            related_object_type='Person',
            )
        db.session.add(personal_context)
        db.session.commit()
      permissions['__GGRC_ADMIN__'] = {
          '__GGRC_ALL__': [personal_context.id,],
          }
    else:
      permissions = {}
    session['permissions'] = permissions

def all_collections():
  """The list of all collections provided by this extension."""
  return [
      service('roles', Role),
      service('users_roles', UserRole),
      ]

