from sqlalchemy import event

from datetime import datetime
from ggrc import db
from sqlalchemy.ext.declarative import declared_attr
from .mixins import deferred
from ggrc.login import get_current_user_id
from .reflection import PublishOnly

class HasObjectState(object):

  _publish_attrs = [
    PublishOnly('os_last_updated_by_user_id'),
    PublishOnly('os_last_updated'),
    PublishOnly('os_approved_on'),
    PublishOnly('os_state'),
  ]

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

  @declared_attr
  def os_last_updated_by_user_id(cls):
    return deferred(db.Column(db.Integer), cls.__name__)

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
    target.os_last_updated_by_user_id = get_current_user_id()

def state_before_update_listener(mapper, connection, target):
  # import ipdb; ipdb.set_trace()
  if hasattr(target, 'os_state'):
    if hasattr(target, 'skip_os_state_update'):
      if target.skip_os_state_update:
        return
    target.os_state = ObjectStates.MODIFIED
    target.os_last_updated = datetime.now()
    target.os_last_updated_by_user_id = get_current_user_id()

def track_state_for_class(object_class):
  event.listen(object_class, 'before_insert', state_before_insert_listener)
  event.listen(object_class, 'before_update', state_before_update_listener)
