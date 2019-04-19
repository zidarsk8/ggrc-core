# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Contains a WithReadOnlyAccess mixin.

It allows to mark objects as read-only
"""

import logging

from sqlalchemy.orm import validates

from ggrc import db
from ggrc.fulltext import attributes
from ggrc.models import reflection
from ggrc.models.exceptions import ValidationError


logger = logging.getLogger(__name__)


class WithReadOnlyAccess(object):
  """Mixin for models which can be marked as read-only"""
  # pylint: disable=too-few-public-methods

  _read_only_model_relationships = (
      'Document'
  )

  readonly = db.Column(db.Boolean, nullable=False, default=False)

  _api_attrs = reflection.ApiAttributes(
      reflection.Attribute("readonly", create=True, update=True),
      reflection.Attribute("external_custom_attributes", read=False),
  )

  _aliases = {
      "readonly": {
          "display_name": "Read-only",
          "mandatory": False,
          "hidden": True,
      },
  }

  _fulltext_attrs = [
      attributes.BooleanFullTextAttr(
          'readonly',
          'readonly',
          true_value="yes",
          false_value="no",
      )
  ]

  def can_change_relationship_with(self, obj):
    """Check whether relationship from self to obj1 can be changed

    This function doesn't expect that another obj also has type
    WithReadOnlyAccess. In this case can_change_relationship_with() of
    another object have to be called also to ensure that relationship is
    not read-only. Final read-only flag can be calculated
    using the following expression:
      obj1.can_change_relationship_with(obj2) and \
      obj2.can_change_relationship_with(obj1)
    """

    if not self.readonly:
      return True

    return obj.__class__.__name__ not in self._read_only_model_relationships

  @validates('readonly')
  def validate_readonly(self, _, value):  # pylint: disable=no-self-use
    """Validate readonly"""
    if value is None:
      # if value is not specified or is set to None, use default value False
      return self.readonly

    if not isinstance(value, bool):
      raise ValidationError("Attribute 'readonly' has invalid value")

    return value

  def external_custom_attributes(self, src):
    # type: (List[Dict[str, str]]) -> None
    """Set CAV in format specific to sync service

    This method accesses only 'external_custom_attributes' key from 'src'

    Format example: [{'name': 'a', value: 'val-a'},
                     {'name': 'b', value: 'val-b'}]
    In this example, values 'val-a' and 'val-b' have to be set to
    custom attributes with names 'a' and 'b' correspondingly

    if `values` is empty, no attributes will be set

    If custom attribute with some name doesn't exist, corresponding item will
    be skipped

    This method calls original `custom_attribute_values` setter

    :param src: json dict from request
    """

    values = src.get('external_custom_attributes')

    if not values:
      return

    cad_ti_map = dict(
        (cad.title, cad.id)
        for cad in self.get_custom_attribute_definitions()
    )

    cavs = list()
    for item in values:
      if 'name' not in item or 'value' not in item:
        continue

      name = item['name']
      value = item['value']
      if name not in cad_ti_map:
        logger.warning("Skipping external custom attribute %r, because "
                       "definition with such name was not found", name)
        continue
      cavs.append({
          'custom_attribute_id': cad_ti_map[name],
          'attribute_value': value,
          'attribute_object': None,
      })

    # pylint: disable=attribute-defined-outside-init
    self.custom_attribute_values = cavs
