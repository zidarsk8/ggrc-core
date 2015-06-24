# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: laran@reciprocitylabs.com
# Maintained By: laran@reciprocitylabs.com

from ggrc import db
from ggrc.models.custom_attribute_value import CustomAttributeValue
from ggrc.models.computed_property import computed_property
from ggrc.models.reflection import PublishOnly
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

  # TODO: People model could use something like this as well
  @computed_property
  def hide_delete_button(self):
    return db.session.query(CustomAttributeValue)\
        .filter(CustomAttributeValue.custom_attribute_id == self.id).count() > 0

  _publish_attrs = [
      'definition_type',
      'attribute_type',
      'multi_choice_options',
      'mandatory',
      'helptext',
      'placeholder',
      PublishOnly('hide_delete_button')
  ]

  class ValidTypes(object):
    TEXT = "Text"
    RICH_TEXT = "Rich Text"
    DROPDOWN = "Dropdown"
    CHECKBOX = "Checkbox"
    DATE = "Date"
