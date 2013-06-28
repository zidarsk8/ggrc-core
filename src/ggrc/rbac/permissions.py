# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

from flask import g
from ggrc.extensions import get_extension_instance

def get_permissions_provider():
  return get_extension_instance(
      'USER_PERMISSIONS_PROVIDER',
      'ggrc.rbac.permissions_provider.DefaultUserPermissionsProvider')

def permissions_for(user):
  return get_permissions_provider().permissions_for(user)

def get_user():
  if hasattr(g, 'user'):
    return g.user
  return None

def is_allowed_create(resource_type, context_id):
  """Whether or not the user is allowed to create a resource of the specified
  type in the context.
  """
  return permissions_for(get_user()).is_allowed_create(
      resource_type, context_id)

def is_allowed_read(resource_type, context_id):
  """Whether or not the user is allowed to read a resource of the specified
  type in the context.
  """
  return permissions_for(get_user()).is_allowed_read(resource_type, context_id)

def is_allowed_update(resource_type, context_id):
  """Whether or not the user is allowed to update a resource of the specified
  type in the context.
  """
  return permissions_for(get_user()).is_allowed_update(
      resource_type, context_id)

def is_allowed_delete(resource_type, context_id):
  """Whether or not the user is allowed to delete a resource of the specified
  type in the context.
  """
  return permissions_for(get_user()).is_allowed_delete(
      resource_type, context_id)

def create_contexts_for(resource_type):
  """All contexts in which the user has create permission."""
  return permissions_for(get_user()).create_contexts_for(resource_type)

def read_contexts_for(resource_type):
  """All contexts in which the user has read permission."""
  return permissions_for(get_user()).read_contexts_for(resource_type)

def update_contexts_for(resource_type):
  """All contexts in which the user has update permission."""
  return permissions_for(get_user()).update_contexts_for(resource_type)

def delete_contexts_for(resource_type):
  """All contexts in which the user has delete permission."""
  return permissions_for(get_user()).delete_contexts_for(resource_type)

