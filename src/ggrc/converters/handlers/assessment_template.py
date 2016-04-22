# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

"""Handlers for special object mappings."""


from sqlalchemy.orm.session import make_transient

from ggrc import db
from ggrc import models
from ggrc.converters.handlers import handlers


class TemplateColumnHandler(handlers.MappingColumnHandler):

  def __init__(self, row_converter, key, **options):
    self.key = key
    self.mapping_object = models.AssessmentTemplate
    self.new_slugs = {}
    super(handlers.MappingColumnHandler, self).__init__(
        row_converter, key, **options)

  def set_obj_attr(self):
    self.value = self.parse_item()
    if not self.dry_run:
      self.create_custom_attributes()

  def insert_object(self):
    pass

  def create_custom_attributes(self):
    table_singular = self.row_converter.obj._inflector.table_singular
    db.session.flush()
    if not self.value:
      return
    template = self.value[0]
    cad = models.CustomAttributeDefinition
    custom_attributes = cad.eager_query().filter(
        cad.definition_type == template._inflector.table_singular,
        cad.definition_id == template.id)
    for attribute_definition in custom_attributes:
      make_transient(attribute_definition)
      attribute_definition.id = None
      attribute_definition.definition_type = table_singular
      attribute_definition.definition_id = self.row_converter.obj.id
      db.session.add(attribute_definition)
    db.session.commit()

  def get_value(self):
    return ""
