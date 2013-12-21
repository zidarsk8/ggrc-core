# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

import datetime
from flask import Blueprint, session, g
import sqlalchemy.orm
from sqlalchemy.orm.attributes import get_history
from sqlalchemy import and_, or_
from ggrc import db, settings
from ggrc.login import get_current_user, login_required
from ggrc.models.audit import Audit
from ggrc.models.context import Context
from ggrc.models.program import Program
from ggrc.rbac import permissions
from ggrc.rbac.permissions_provider import DefaultUserPermissions
from ggrc.services.registry import service
from ggrc.services.common import Resource
from ggrc.views import object_view
from . import basic_roles
from .models import Role, RoleImplication, UserRole

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
    ret = UserPermissions()
    # force the permissions to be loaded into session, otherwise templates
    # that depend on the permissions being available in session may assert
    # the user has no permissions!
    ret.check_permissions()
    return ret

  def handle_admin_user(self, user):
    pass

class BasicUserPermissions(DefaultUserPermissions):
  """User permissions that aren't kept in session."""
  def __init__(self, user):
    self.user = user
    self.permissions = load_permissions_for(user)

  def _permissions(self):
    return self.permissions

class UserPermissions(DefaultUserPermissions):
  @property
  def _request_permissions(self):
    return getattr(g, '_request_permissions', None)

  @_request_permissions.setter
  def _request_permissions(self, value):
    setattr(g, '_request_permissions', value)

  def _permissions(self):
    self.check_permissions()
    return self._request_permissions

  def check_permissions(self):
    if not self._request_permissions:
      self.load_permissions()

  def get_email_for(self, user):
    return user.email if hasattr(user, 'email') else 'ANONYMOUS'

  def load_permissions(self):
    user = get_current_user()
    email = self.get_email_for(user)
    self._request_permissions = {}
    self._request_permissions['__user'] = email
    if user is None or user.is_anonymous():
      self._request_permissions = {}
    else:
      self._request_permissions = load_permissions_for(user)

def collect_permissions(src_permissions, context_id, permissions):
  for action, resource_permissions in src_permissions.items():
    if not resource_permissions:
      permissions.setdefault(action, dict())
    for resource_permission in resource_permissions:
      if type(resource_permission) in [str, unicode]:
        resource_type = str(resource_permission)
        condition = None
      else:
        resource_type = str(resource_permission['type'])
        condition = resource_permission.get('condition', None)
        terms = resource_permission.get('terms', [])
      permissions.setdefault(action, {})\
          .setdefault(resource_type, dict())\
          .setdefault('contexts', list())\
          .append(context_id)
      if condition:
        permissions[action][resource_type]\
            .setdefault('conditions', dict())\
            .setdefault(context_id, list())\
            .append({
              'condition': condition,
              'terms': terms,
              })

def load_permissions_for(user):
  """Permissions is dictionary that can be exported to json to share with
  clients. Structure is:
  ..

    permissions[action][resource_type][contexts]
                                      [conditions][context][context_conditions]

  'action' is one of 'create', 'read', 'update', 'delete'.
  'resource_type' is the name of a valid gGRC resource type.
  'contexts' is a list of context_id where the action is allowed.
  'conditions' is a dictionary of 'context_conditions' indexed by 'context'
    where 'context' is a context_id.
  'context_conditions' is a list of dictionaries with 'condition' and 'terms'
    keys.
  'condition' is the string name of a conditional operator, such as 'contains'.
  'terms' are the arguments to the 'condition'.
  """
  permissions = {}

  # Add default `Help` permissions for everyone, always
  help_permissions = { "read": [ "Help" ] }
  collect_permissions(help_permissions, None, permissions)

  # Add `ADMIN_PERMISSION` for "bootstrap admin" users
  if hasattr(settings, 'BOOTSTRAP_ADMIN_USERS') \
      and user.email in settings.BOOTSTRAP_ADMIN_USERS:
    admin_permissions = {
        DefaultUserPermissions.ADMIN_PERMISSION.action: [
          DefaultUserPermissions.ADMIN_PERMISSION.resource_type
          ]
        }
    collect_permissions(
        admin_permissions,
        DefaultUserPermissions.ADMIN_PERMISSION.context_id,
        permissions)

  # Now add permissions from all DB-managed roles
  user_roles = db.session.query(UserRole)\
      .options(
          sqlalchemy.orm.undefer_group('UserRole_complete'),
          sqlalchemy.orm.undefer_group('Role_complete'),
          sqlalchemy.orm.joinedload('role'))\
      .filter(UserRole.person_id==user.id)\
      .order_by(UserRole.updated_at.desc())\
      .all()
  roles_contexts = {}
  for user_role in user_roles:
    roles_contexts.setdefault(user_role.role_id, set())
    roles_contexts[user_role.role_id].add(user_role.context_id)
    if isinstance(user_role.role.permissions, dict):
      collect_permissions(
          user_role.role.permissions, user_role.context_id, permissions)

  # Collate roles/contexts to eager load all required implications
  implications_queries = []
  for role_id, context_ids in roles_contexts.items():
    if None in context_ids:
      implications_queries.append(and_(
        RoleImplication.source_role_id == role_id,
        RoleImplication.source_context_id == None))
      context_ids.remove(None)
    if len(context_ids) > 0:
      implications_queries.append(and_(
        RoleImplication.source_role_id == role_id,
        RoleImplication.source_context_id.in_(context_ids)))
  if len(implications_queries) > 0:
    implications = RoleImplication.query\
        .filter(or_(*implications_queries))\
        .options(
            sqlalchemy.orm.undefer_group('Role_complete'),
            sqlalchemy.orm.joinedload('role'))\
        .all()
  else:
    implications = []

  for implication in implications:
    if isinstance(implication.role.permissions, dict):
      collect_permissions(
          implication.role.permissions, implication.context_id, permissions)

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
  permissions.setdefault('__GGRC_ADMIN__',{})\
      .setdefault('__GGRC_ALL__', dict())\
      .setdefault('contexts', list())\
      .append(personal_context.id)
  return permissions

def all_collections():
  """The list of all collections provided by this extension."""
  return [
      service('roles', Role),
      service('user_roles', UserRole),
      ]

@Resource.model_posted.connect_via(Program)
def handle_program_post(sender, obj=None, src=None, service=None):
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
  context.related_object = obj
  db.session.add(context)
  db.session.flush()
  obj.context = context

  # add a user_roles mapping assigning the user creating the program
  # the ProgramOwner role in the program's context.
  program_owner_role = basic_roles.program_owner()
  user_role = UserRole(
      person=get_current_user(),
      role=program_owner_role,
      context=context,
      )
  db.session.add(user_role)
  db.session.flush()

  assign_role_reader(get_current_user())
  if not src.get('private'):
    # Add role implication - all users can read a public program
    add_public_program_role_implication(basic_roles.reader(), context)
    add_public_program_role_implication(basic_roles.object_editor(), context)
    add_public_program_role_implication(basic_roles.program_creator(), context)
  #add_role_reader_implications(basic_roles.program_reader(), context)
  #add_role_reader_implications(basic_roles.program_editor(), context)
  #add_role_reader_implications(basic_roles.program_owner(), context)

def add_role_reader_implications(source_role, context):
  db.session.add(RoleImplication(
    source_context=context,
    source_role=source_role,
    role=basic_roles.program_basic_reader(),
    context=None,
    modified_by=get_current_user(),
    ))

def add_public_program_role_implication(
    source_role, context, check_exists=False):
  if check_exists and db.session.query(RoleImplication)\
      .filter(
          and_(
            RoleImplication.context_id == context.id,
            RoleImplication.source_context_id == None))\
      .count() > 0:
    return
  db.session.add(RoleImplication(
    source_context=None,
    source_role=source_role,
    context=context,
    role=basic_roles.program_reader(),
    modified_by=get_current_user(),
    ))

@Resource.model_put.connect_via(Program)
def handle_program_put(sender, obj=None, src=None, service=None):
  #Check to see if the private property of the program has changed
  if get_history(obj, 'private').has_changes():
    if obj.private:
      #ensure that any implications from null context are removed
      implications = db.session.query(RoleImplication)\
          .filter(
              RoleImplication.context_id == obj.context_id,
              RoleImplication.source_context_id == None)\
                  .delete()
      db.session.flush()
    else:
      #ensure that implications from null are present
      add_public_program_role_implication(
          basic_roles.reader(), obj.context, check_exists=True)
      add_public_program_role_implication(
          basic_roles.object_editor(), obj.context, check_exists=True)
      add_public_program_role_implication(
          basic_roles.program_creator(), obj.context, check_exists=True)
      db.session.flush()

@Resource.model_posted.connect_via(Audit)
def handle_audit_post(sender, obj=None, src=None, service=None):
  #Create an audit context
  context = Context(
      context=obj.context,
      name='Audit Context {timestamp}'.format(
        timestamp=datetime.datetime.now()),
      description='',
      modified_by=get_current_user(),
      )
  db.session.add(context)

  #Create the role implications
  if obj.context and obj.context.id is not None:
    create_private_program_audit_role_implications(obj.context, context)
  else:
    create_public_program_audit_role_implications(context)
  #Create the role implication for Auditor from Audit for default context
  db.session.add(RoleImplication(
      source_context=context,
      source_role=basic_roles.auditor(),
      role=basic_roles.auditor_reader(),
      context=None,
      modified_by=get_current_user(),
      ))
  db.session.flush()

  #Place the audit in the audit context
  obj.context = context

def create_private_program_audit_role_implications(
    program_context, audit_context):
  #Roles implied from Private Program context for Audit context
  db.session.add(RoleImplication(
      source_context=program_context,
      source_role=basic_roles.program_owner(),
      context=audit_context,
      role=basic_roles.program_audit_owner(),
      modified_by=get_current_user(),
      ))
  db.session.add(RoleImplication(
      source_context=program_context,
      source_role=basic_roles.program_editor(),
      role=basic_roles.program_audit_editor(),
      context=audit_context,
      modified_by=get_current_user(),
      ))
  db.session.add(RoleImplication(
      source_context=program_context,
      source_role=basic_roles.program_reader(),
      role=basic_roles.program_audit_reader(),
      context=audit_context,
      modified_by=get_current_user(),
      ))
  #Role implied from Audit for Private Program context
  db.session.add(RoleImplication(
      source_context=audit_context,
      source_role=basic_roles.auditor(),
      role=basic_roles.auditor_program_reader(),
      context=program_context,
      modified_by=get_current_user(),
      ))

def create_public_program_audit_role_implications(audit_context):
  #Roles implied from Private Program context for Audit context
  db.session.add(RoleImplication(
      source_context=None,
      source_role=basic_roles.object_editor(),
      context=audit_context,
      role=basic_roles.program_audit_editor(),
      modified_by=get_current_user(),
      ))
  db.session.add(RoleImplication(
      source_context=None,
      source_role=basic_roles.reader(),
      role=basic_roles.program_audit_reader(),
      context=audit_context,
      modified_by=get_current_user(),
      ))

@Resource.model_posted.connect_via(UserRole)
def handle_program_owner_role_assignment(
    sender, obj=None, src=None, service=None):
  if 'read' in obj.role.permissions and \
      'UserRole' in obj.role.permissions['read']:
    # Make sure that the user can read roles, too
    assign_role_reader(obj.person)

def assign_role_reader(user):
    role_reader_role = db.session.query(Role)\
        .filter(Role.name == 'RoleReader').first()
    user_permissions = BasicUserPermissions(user)
    if not user_permissions.is_allowed_read('Role', None):
      role_reader_for_user = UserRole(
          person_id=user.id,
          role=role_reader_role,
          context_id=None,
          )
      db.session.add(role_reader_for_user)

# Removed because this is now handled purely client-side, but kept
# here as a reference for the next one.
# @BaseObjectView.extension_contributions.connect_via(Program)
def contribute_to_program_view(sender, obj=None, context=None):
  if obj.context_id != None and \
      permissions.is_allowed_read('Role', 1) and \
      permissions.is_allowed_read('UserRole', obj.context_id) and \
      permissions.is_allowed_create('UserRole', obj.context_id) and \
      permissions.is_allowed_update('UserRole', obj.context_id) and \
      permissions.is_allowed_delete('UserRole', obj.context_id):
    return 'permissions/programs/_role_assignments.haml'
  return None

from ggrc.app import app
@app.context_processor
def authorized_users_for():
  return {'authorized_users_for': UserRole.role_assignments_for,}

def initialize_all_object_views(app):
  role_view_entry = object_view(Role)
  role_view_entry.service_class.add_to(
      app,
      '/{0}'.format(role_view_entry.url),
      role_view_entry.model_class,
      decorators=(login_required,),
      )
