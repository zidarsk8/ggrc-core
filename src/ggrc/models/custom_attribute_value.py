# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: laran@reciprocitylabs.com
# Maintained By: laran@reciprocitylabs.com

from ggrc import db
from ggrc.models.mixins import Base
from ggrc.models.mixins import deferred


class CustomAttributeValue(Base, db.Model):
  __tablename__ = 'custom_attribute_values'

  custom_attribute_id = deferred(
      db.Column(db.Integer, db.ForeignKey('custom_attribute_definitions.id',
                                          ondelete="CASCADE")),
      'CustomAttributeValue')
  attributable_id = deferred(db.Column(db.Integer), 'CustomAttributeValue')
  attributable_type = deferred(db.Column(db.String), 'CustomAttributeValue')
  attribute_value = deferred(db.Column(db.String), 'CustomAttributeValue')

  @property
  def attributable_attr(self):
    return '{0}_attributable'.format(self.attributable_type)

  @property
  def attributable(self):
    return getattr(self, self.attributable_attr)

  @attributable.setter
  def attributable(self, value):
    self.attributable_id = value.id if value is not None else None
    self.attributable_type = value.__class__.__name__ if value is not None \
        else None
    return setattr(self, self.attributable_attr, value)

  _publish_attrs = [
      'custom_attribute_id',
      'attributable_id',
      'attributable_type',
      'attribute_value'
  ]

  @classmethod
  def mk_filter_by_custom(cls, obj_class, custom_attribute_id):
    def filter_by(predicate):
      return cls.query.filter(
          (cls.custom_attribute_id == custom_attribute_id) &
          (cls.attributable_type == obj_class.__name__) &
          (cls.attributable_id == obj_class.id) &
          predicate(cls.attribute_value)
      ).exists()
    return filter_by
