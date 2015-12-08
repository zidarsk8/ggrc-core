# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

from sqlalchemy import event

from datetime import datetime
from ggrc import db
from sqlalchemy.ext.declarative import declared_attr
from .mixins import deferred
from ggrc.login import get_current_user_id
from .reflection import PublishOnly

class HasObjectState(object):

  _publish_attrs = [
    PublishOnly('os_state'),
  ]

  def __init__(self, *args, **kwargs):
    self._skip_os_state_update = False;
    super(HasObjectState, self).__init__(*args, **kwargs)

  @declared_attr
  def os_state(cls):
    return deferred(db.Column(db.String, nullable=False, default=ObjectStates.DRAFT), cls.__name__)

  def skip_os_state_update(self):
    self._skip_os_state_update = True

class ObjectStates:
  DRAFT = 'Draft'
  APPROVED = 'Approved'
  DECLINED = 'Declined'
  MODIFIED = 'Modified'

# This table
class ObjectStateTables:
  table_names = [
    'programs', 'objectives', 'controls', 'sections',
    'systems', 'data_assets', 'facilities',
    'markets', 'products', 'projects', 'directives',
    'org_groups', 'vendors'
  ]

def state_before_insert_listener(mapper, connection, target):
  if hasattr(target, 'os_state'):
    target.os_state = ObjectStates.DRAFT

def state_before_update_listener(mapper, connection, target):
  if hasattr(target, 'os_state'):
    if hasattr(target, '_skip_os_state_update'):
      if True == target._skip_os_state_update:
        return
    target.os_state = ObjectStates.MODIFIED

def track_state_for_class(object_class):
  event.listen(object_class, 'before_insert', state_before_insert_listener)
  event.listen(object_class, 'before_update', state_before_update_listener)
