# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

from ggrc import db
from ggrc.models.mixins import deferred, Base, Described

class Context(Described, Base, db.Model):
  __tablename__ = 'contexts'

  name = deferred(db.Column(db.String(128), nullable=True), 'Context')
  related_object_id = deferred(
      db.Column(db.Integer(), nullable=True), 'Context')
  related_object_type = deferred(
      db.Column(db.String(128), nullable=True), 'Context')

  @property
  def related_object(self):
    self._related_object = None
    if not hasattr(self, '_related_object'):
      if self.related_object_type:
        import ggrc.models
        import ggrc.utils
        service = ggrc.utils.service_for(str(self.related_object_type))
        model_class = service._model
        if self.related_object_id:
          self._related_object = db.session.query(model_class)\
              .get(self.related_object_id)
    return self._related_object

  @related_object.setter
  def related_object(self, obj):
    if obj is not None:
      self.related_object_id = obj.id
      self.related_object_type = obj.__class__.__name__
    else:
      self.related_object_id = None
      self.related_object_type = None
    self._related_object = obj

  _publish_attrs = ['name', 'related_object',]
  _sanitize_html = ['name',]
  _include_links = []
