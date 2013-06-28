# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

from ggrc import db

class Role(db.Model):
  """A user role. All roles have a unique name. This name could be a simple
  string, an email address, or some other form of string identifier.
  """
  __tablename__ = 'roles'

  name  = db.Column(db.String(128), primary_key=True)
  description = db.Column(db.Text())
  permissions = db.relationship('RolePermission', backref='role')

  _publish_attrs = ['name', 'description', 'permissions',]

class RolePermission(db.Model):
  """Mapping of role to (permission, resource_type, context_id) tuples"""
  __tablename__ = 'roles_permissions'

  role_name = db.Column(
      db.String(128), db.ForeignKey('roles.name'), primary_key=True)
  action = db.Column(db.String(6), primary_key=True)
  resource_type = db.Column(db.String(), primary_key=True)
  context_id = db.Column(db.Integer, primary_key=True)

  _publish_attrs = ['role', 'action', 'resource_type', 'context_id',]

class UserRole(db.Model):
  __tablename__ = 'users_roles'

  role_name = db.Column(
      db.String(128), db.ForeignKey('roles.name'), primary_key=True)
  user_id = db.Column(db.String(128), primary_key=True)
  role = db.relationship('roles')

  _publish_attrs = ['role', 'user_id']
