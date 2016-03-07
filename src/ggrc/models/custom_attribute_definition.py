# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: laran@reciprocitylabs.com
# Maintained By: laran@reciprocitylabs.com

from sqlalchemy.sql.schema import UniqueConstraint

from ggrc import db

from .mixins import (
    deferred, Titled, Base
)


class CustomAttributeDefinition(Base, Titled, db.Model):
  __tablename__ = 'custom_attribute_definitions'

  definition_type = deferred(db.Column(db.String), 'CustomAttributeDefinition')
  attribute_type = deferred(db.Column(db.String), 'CustomAttributeDefinition')
  multi_choice_options = deferred(db.Column(db.String),
                                  'CustomAttributeDefinition')
  mandatory = deferred(db.Column(db.Boolean), 'CustomAttributeDefinition')
  helptext = deferred(db.Column(db.String), 'CustomAttributeDefinition')
  placeholder = deferred(db.Column(db.String), 'CustomAttributeDefinition')

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
