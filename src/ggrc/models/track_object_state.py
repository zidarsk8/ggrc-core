from sqlalchemy import event

from datetime import datetime
from ggrc import db
from sqlalchemy.ext.declarative import declared_attr
from .mixins import deferred

class HasObjectState(object):

  def __init__(self):
    self._skip_os_state_update = False;

  @declared_attr
  def os_state(cls):
    return deferred(db.Column(db.String, nullable=False), cls.__name__)

  @declared_attr
  def os_last_updated(cls):
    return deferred(db.Column(db.DateTime, nullable=False), cls.__name__)

  @declared_attr
  def os_approved_on(cls):
    return deferred(db.Column(db.DateTime), cls.__name__)

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
    'markets', 'products', 'projects', 'directives'
  ]

def state_before_insert_listener(mapper, connection, target):
  if hasattr(target, 'os_state'):
    target.os_state = ObjectStates.DRAFT
    target.os_last_updated = datetime.now()

def state_before_update_listener(mapper, connection, target):
  # import ipdb; ipdb.set_trace()
  if hasattr(target, 'os_state'):
    if hasattr(target, 'skip_os_state_update'):
      if target.skip_os_state_update:
        return
    target.os_state = ObjectStates.MODIFIED
    target.os_last_updated = datetime.now()

def track_state_for_class(object_class):
  event.listen(object_class, 'before_insert', state_before_insert_listener)
  event.listen(object_class, 'before_update', state_before_update_listener)
