# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: laran@reciprocitylabs.com
# Maintained By: laran@reciprocitylabs.com

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql.schema import UniqueConstraint

from ggrc import db
from ggrc.models import mixins
from ggrc.models.custom_attribute_value import CustomAttributeValue


class CustomAttributeDefinition(mixins.Base, mixins.Titled, db.Model):
  __tablename__ = 'custom_attribute_definitions'

  definition_type = db.Column(db.String)
  attribute_type = db.Column(db.String)
  multi_choice_options = db.Column(db.String)
  mandatory = db.Column(db.Boolean)
  helptext = db.Column(db.String)
  placeholder = db.Column(db.String)

  attribute_values = db.relationship('CustomAttributeValue',
                                     backref='custom_attribute')

  __table_args__ = (UniqueConstraint(
      'title', 'definition_type', name='_unique_attribute'),)

  _publish_attrs = [
      'definition_type',
      'attribute_type',
      'multi_choice_options',
      'mandatory',
      'helptext',
      'placeholder',
  ]

  class ValidTypes(object):
    TEXT = "Text"
    RICH_TEXT = "Rich Text"
    DROPDOWN = "Dropdown"
    CHECKBOX = "Checkbox"
    DATE = "Date"
    MAP = "Map"


class CustomAttributeMapable(object):
  # pylint: disable=too-few-public-methods
  # because this is a mixin

  @declared_attr
  def related_custom_attributes(self):
    return db.relationship(
        'CustomAttributeValue',
        primaryjoin=lambda: (
            (CustomAttributeValue.attribute_value == self.__name__) &
            (CustomAttributeValue.attribute_object_id == self.id)),
        foreign_keys="CustomAttributeValue.attribute_object_id",
        backref='attribute_{0}'.format(self.__name__),
        viewonly=True)
