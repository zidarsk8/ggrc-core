# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: laran@reciprocitylabs.com
# Maintained By: laran@reciprocitylabs.com

from ggrc import db
from .mixins import (
    deferred, Titled, Base
    )

class CustomAttributeDefinition(Base, Titled, db.Model):
  __tablename__ = 'custom_attribute_definitions'

  type_string = deferred(db.Column(db.String), 'CustomAttributeDefinition')
  multi_choice_options = deferred(db.Column(db.String), 'CustomAttributeDefinition')
  mandatory = deferred(db.Column(db.Boolean), 'CustomAttributeDefinition')

  _publish_attrs = [
      'type_string',
      'multi_choice_options',
      'mandatory'
      ]
