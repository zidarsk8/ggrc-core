# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from sqlalchemy import event

from ggrc import db
from sqlalchemy.ext.declarative import declared_attr
from ggrc.models.deferred import deferred
from ggrc.models.reflection import PublishOnly


class HasObjectState(object):

  _publish_attrs = [
      PublishOnly('os_state'),
  ]

  def __init__(self, *args, **kwargs):
    self._skip_os_state_update = False
    super(HasObjectState, self).__init__(*args, **kwargs)

  @declared_attr
  def os_state(cls):
    return deferred(db.Column(db.String, nullable=False,
                              default=ObjectStates.DRAFT), cls.__name__)

  def skip_os_state_update(self):
    self._skip_os_state_update = True


class ObjectStates:
  DRAFT = 'Draft'
  APPROVED = 'Approved'
  DECLINED = 'Declined'
  MODIFIED = 'Modified'


def state_before_insert_listener(mapper, connection, target):
  if hasattr(target, 'os_state'):
    target.os_state = ObjectStates.DRAFT


def state_before_update_listener(mapper, connection, target):
  if hasattr(target, 'os_state'):
    if getattr(target, '_skip_os_state_update', None) is True:
      return
    target.os_state = ObjectStates.MODIFIED


def track_state_for_class(object_class):
  event.listen(object_class, 'before_insert', state_before_insert_listener)
  event.listen(object_class, 'before_update', state_before_update_listener)
