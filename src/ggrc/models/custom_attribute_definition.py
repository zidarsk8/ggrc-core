# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Custom attribute definition module"""

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import validates
from sqlalchemy.sql.schema import UniqueConstraint

import ggrc.models
from ggrc import db
from ggrc.models import mixins
from ggrc.models.reflection import AttributeInfo
from ggrc.models.custom_attribute_value import CustomAttributeValue
from ggrc.models.exceptions import ValidationError


class CustomAttributeDefinition(mixins.Base, mixins.Titled, db.Model):
  """Custom attribute definition model.

  Attributes:
    multi_choice_mandatory: comma separated values of mandatory bitmaps.
      First lsb is for comment, second bit is for attachement.
  """

  __tablename__ = 'custom_attribute_definitions'

  definition_type = db.Column(db.String, nullable=False)
  definition_id = db.Column(db.Integer)
  attribute_type = db.Column(db.String, nullable=False)
  multi_choice_options = db.Column(db.String)
  multi_choice_mandatory = db.Column(db.String)
  mandatory = db.Column(db.Boolean)
  helptext = db.Column(db.String)
  placeholder = db.Column(db.String)

  attribute_values = db.relationship('CustomAttributeValue',
                                     backref='custom_attribute')

  _extra_table_args = (
      UniqueConstraint('definition_type', 'definition_id', 'title',
                       name='uq_custom_attribute'),
      db.Index('ix_custom_attributes_title', 'title'))

  _include_links = _publish_attrs = [
      'definition_type',
      'definition_id',
      'attribute_type',
      'multi_choice_options',
      'multi_choice_mandatory',
      'mandatory',
      'helptext',
      'placeholder',
  ]

  _reserved_names = {}

  def _clone(self, target):
    """Clone custom attribute definitions."""
    data = {
        "title": self.title,
        "definition_type": self.definition_type,
        "definition_id": target.id,
        "attribute_type": self.attribute_type,
        "multi_choice_options": self.multi_choice_options,
        "multi_choice_mandatory": self.multi_choice_mandatory,
        "mandatory": self.mandatory,
        "helptext": self.helptext,
        "placeholder": self.placeholder,
    }
    ca_definition = CustomAttributeDefinition(**data)
    db.session.add(ca_definition)
    db.session.flush()
    return ca_definition

  class ValidTypes(object):
    """Class representing valid custom attribute definitions.

    Basically an enum, therefore no need for public methods.
    """
    # pylint: disable=too-few-public-methods
    TEXT = "Text"
    RICH_TEXT = "Rich Text"
    DROPDOWN = "Dropdown"
    CHECKBOX = "Checkbox"
    DATE = "Date"
    MAP = "Map"

  class MultiChoiceMandatoryFlags(object):
    """Enum representing flags in multi_choice_mandatory bitmaps."""
    # pylint: disable=too-few-public-methods
    COMMENT_REQUIRED = 0b01
    EVIDENCE_REQUIRED = 0b10

  VALID_TYPES = {
      "Text": "Text",
      "Rich Text": "Rich Text",
      "Dropdown": "Dropdown",
      "Checkbox": "Checkbox",
      "Date": "Date",
      "Person": "Map:Person",
  }

  @validates("attribute_type")
  def validate_attribute_type(self, _, value):
    """Check that provided attribute_type is allowed."""
    if value not in self.VALID_TYPES.values():
      raise ValidationError("Invalid attribute_type: got {v}, "
                            "expected one of {l}"
                            .format(v=value,
                                    l=list(self.VALID_TYPES.values())))
    return value

  @validates("multi_choice_options")
  def validate_multi_choice_options(self, _, value):
    """Strip spaces around options in dropdown options."""
    # pylint: disable=no-self-use
    # TODO: this should be "if value is not None" to disallow value == ""
    if value:
      value_list = [part.strip() for part in value.split(",")]
      value_set = set(value_list)
      if len(value_set) != len(value_list):
        raise ValidationError("Duplicate dropdown options are not allowed: "
                              "'{}'".format(value))
      if "" in value_set:
        raise ValidationError("Empty dropdown options are not allowed: '{}'"
                              .format(value))
      value = ",".join(value_list)

    return value

  @validates("multi_choice_mandatory")
  def validate_multi_choice_mandatory(self, _, value):
    """Strip spaces around bitmas in dropdown options."""
    # pylint: disable=no-self-use
    if value:
      value = ",".join(part.strip() for part in value.split(","))

    return value

  @classmethod
  def _get_reserved_names(cls, definition_type):
    """Get a list of all attribute names in all objects.

    On first call this function computes all possible names that can be used by
    any model and stores them in a static frozen set. All later calls just get
    this set.

    Returns:
      frozen set containing all reserved attribute names for the current object.
    """
    if not cls._reserved_names.get(definition_type):
      definition_model = getattr(ggrc.models.all_models, definition_type, None)
      if not definition_model:
        raise ValueError("Invalid definition type")

      aliases = AttributeInfo.gather_aliases(definition_model)
      cls._reserved_names[definition_type] = frozenset(
        (value["display_name"] if isinstance(value, dict) else value).lower()
        for value in aliases.values() if value
      )
    return cls._reserved_names[definition_type]

  @classmethod
  def _get_global_cad_names(cls, definition_type):
    query = db.session.query(cls.title).filter(
      cls.definition_type == definition_type,
      cls.definition_id.is_(None)
    )

    return set(item[0] for item in query)

  @validates("title", "definition_type")
  def validate_title(self, key, value):
    """Validate CAD title/name uniqueness.

    Note: title field is used for storing CAD names.
    CAD names need to follow 3 uniqueness rules:
      1) names must not match any attribute name on any existing object.
      2) Object level CAD names must not match any global CAD name.
      3) Object level CAD names can clash, but not for the same Object
         instance. This means we can have two CAD with a name "my cad", with
         different attributable_id fields.

    Third rule is handled by the database with unique key uq_custom_attribute
    (`definition_type`,`definition_id`,`title`).

    This validator should check for name collisions for 1st and 2nd rule.

    This validator works, because definition_type is never changed. It only gets
    set when the cad is created and after that only title filed can change.
    This makes validation using both fields possible.

    Args:
      value: custom attribute definition name

    Returns:
      value if the name passes all uniqueness checks.
    """

    if key == "title" and self.definition_type:
      name = value.lower()
      definition_type = self.definition_type
    elif key == "definition_type" and self.title:
      name = self.title
      definition_type = value.lower()
    else:
      return value

    if (name in self._get_reserved_names(definition_type) or
        name in self._get_global_cad_names(definition_type)):
      raise ValueError("Invalid Custom attribute name.")
    return value

class CustomAttributeMapable(object):
  # pylint: disable=too-few-public-methods
  # because this is a mixin

  @declared_attr
  def related_custom_attributes(self):
    """CustomAttributeValues that directly map to this object.

    Used just to get the backrefs on the CustomAttributeValue object.

    Returns:
       a sqlalchemy relationship
    """
    return db.relationship(
        'CustomAttributeValue',
        primaryjoin=lambda: (
            (CustomAttributeValue.attribute_value == self.__name__) &
            (CustomAttributeValue.attribute_object_id == self.id)),
        foreign_keys="CustomAttributeValue.attribute_object_id",
        backref='attribute_{0}'.format(self.__name__),
        viewonly=True)
