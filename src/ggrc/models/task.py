# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

from ggrc import db
from .mixins import deferred, Base, Stateful
from .types import JsonType

class Task(Base, Stateful, db.Model):
  __tablename__ = 'tasks'
  
  VALID_STATES = [
    "Pending",
    "Running",
    "Success",
    "Failure"
  ]
  name = deferred(db.Column(db.String), 'Task')
  parameters = deferred(db.Column(JsonType), 'Task')
  result = deferred(db.Column(db.Text), 'Task')
  
  