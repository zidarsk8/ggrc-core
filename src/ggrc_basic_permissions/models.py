# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

import json
from ggrc import db
from ggrc.builder import simple_property
from ggrc.models.mixins import Base, Described

class Role(Base, Described, db.Model):
  """A user role. All roles have a unique name. This name could be a simple
  string, an email address, or some other form of string identifier.
  
  :permissions:
    example -
      { 'create': ['Program', 'Control'],
        'read': ['Program', 'Control'],
        'update': ['Program', 'Control'],
        'delete': ['Program']
      }
  """
  __tablename__ = 'roles'

  name  = db.Column(db.String(128), nullable=False)
  permissions_json = db.Column(db.Text(), nullable=False)

  @simple_property
  def permissions(self):
    return json.loads(self.permissions_json)

  @permissions.setter
  def permissions(self, value):
    self.permissions_json = json.dumps(value)

  _publish_attrs = ['name', 'permissions']

class UserRole(Base, db.Model):
  __tablename__ = 'users_roles'

  role_id = db.Column(db.Integer(), db.ForeignKey('roles.id'), nullable=False)
  user_email = db.Column(db.String(128), nullable=False)
  role = db.relationship('Role')

  _publish_attrs = ['role', 'user_email',]

