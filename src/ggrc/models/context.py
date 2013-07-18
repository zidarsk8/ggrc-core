# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

from ggrc import db
from ggrc.models.mixins import Base, Described

class Context(Base, Described, db.Model):
  __tablename__ = 'contexts'

  name = db.Column(db.String(128), nullable=True)
  related_object_id = db.Column(db.Integer(), nullable=True)
  related_object_type = db.Column(db.String(128), nullable=True)

  @property
  def related(self, obj=[]):
    if len(obj) == 0:
      if self.related_object_type is not None:
        import ggrc.models
        import ggrc.services.util
        service = ggrc.services.util.service_for(self.related_object_type)
        model_class = service._model
        obj.append(db.session.query(model_class).get(self.related_object_id))
      else:
        obj.append(None)
    return obj[0]

  @related.setter
  def related(self, obj):
    if obj is not None:
      self.related_object_id = obj.id
      self.related_object_type = obj.__class__.__name__
    else:
      self.related_object_id = None
      self.related_object_type = None

  _publish_attrs = ['name', 'related',]

