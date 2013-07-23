# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

import datetime
from flask import session, Blueprint
from ggrc import db, settings
from ggrc.login import get_current_user
from ggrc.models.context import Context
from ggrc.models.program import Program
from ggrc.rbac import permissions
from ggrc.rbac.permissions_provider import DefaultUserPermissions
from ggrc.services.registry import service
from ggrc.services.common import Resource
from ggrc.views.common import BaseObjectView
from .models import Role, UserRole

blueprint = Blueprint(
    'permissions',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/ggrc_basic_permissions',
    )

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
          UserRole.person_id==user.id).all()
      for user_role in user_roles:
        for action, resource_types in user_role.role.permissions.items():
          for resource_type in resource_types:
            permissions.setdefault(action, {}).setdefault(resource_type, [])\
                .append(user_role.context_id)
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
      service('user_roles', UserRole),
      ]

@Resource.model_posted.connect_via(Program)
def handle_program_post(sender, obj=None, src=None, service=None):
  if 'private' in src:
    # get the personal context for this logged in user
    personal_context = service.personal_context()

    # create a context specific to the program
    context = Context(
        context=personal_context,
        name='{object_type} Context {timestamp}'.format(
          object_type=service.model.__name__,
          timestamp=datetime.datetime.now()),
        description='',
        )
    db.session.add(context)
    db.session.flush()
    obj.context = context

    # add a user_roles mapping assigning the user creating the program
    # the ProgramOwner role in the program's context.
    current_user_id = get_current_user().id
    program_owner_role = db.session.query(Role)\
        .filter(Role.name == 'ProgramOwner').first()
    user_role = UserRole(
        person=get_current_user(),
        role=program_owner_role,
        context=context,
        )
    db.session.add(user_role)
    db.session.flush()

    # assign the user RoleReader if they don't already have that role
    role_reader_role = db.session.query(Role)\
        .filter(Role.name == 'RoleReader').first()
    role_reader_for_user = db.session.query(UserRole)\
        .join(Role, UserRole.role == role_reader_role)\
        .filter(UserRole.person_id == current_user_id\
            and Role.name == 'RoleReader')\
        .first()
    if not role_reader_for_user:
      role_reader_for_user = UserRole(
          person_id=current_user_id,
          role=role_reader_role,
          context_id=1,
          )
      db.session.add(role_reader_for_user)
      db.session.flush()

@BaseObjectView.extension_contributions.connect_via(Program)
def contribute_to_program_view(sender, obj=None, context=None):
  print 'contribute_to_program_view', obj
  print session['permissions']
  if obj.context_id != None and \
      permissions.is_allowed_read(Role, 1) and \
      permissions.is_allowed_read(UserRole, obj.context_id) and \
      permissions.is_allowed_create(UserRole, obj.context_id) and \
      permissions.is_allowed_update(UserRole, obj.context_id) and \
      permissions.is_allowed_delete(UserRole, obj.context_id):
    return 'permissions/programs/_role_assignments.haml'
  return None

from ggrc.app import app
@app.context_processor
def authorized_users_for():
  return {'authorized_users_for': UserRole.role_assignments_for,}

