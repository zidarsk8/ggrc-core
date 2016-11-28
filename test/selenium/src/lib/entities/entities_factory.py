# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Module for factories that create business entities."""
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
# pylint: disable=no-self-use
import random

from lib.constants import objects
from lib.constants.element import AttributesTypes
from lib.entities import entity
from lib.utils import string_utils
from lib.utils.string_utils import random_list_of_strings, random_string
from lib.utils.test_utils import append_random_string


class CAFactory(object):
  """Factory class for Custom Attribute entity."""

  @classmethod
  def create(cls, title=None, ca_type=None, definition_type=None,
             helptext="", placeholder=None, multi_choice_options=None,
             is_mandatory=False, ca_global=True):
    """Create CustomAttribute object.

    Random values will be used for title, ca_type, definition_type and
    multi_choice_options if they are None.
    """
    ca_entity = cls._create_random_ca()
    ca_entity = cls._fill_ca_entity_fields(
        ca_entity, title=title, ca_type=ca_type,
        definition_type=definition_type,
        helptext=helptext, placeholder=placeholder,
        multi_choice_options=multi_choice_options, is_mandatory=is_mandatory,
        ca_global=ca_global
    )
    ca_entity = cls._normalize_ca_definition_type(ca_entity)
    return ca_entity

  @classmethod
  def _create_random_ca(cls):
    """Create CustomAttribute entity with randomly filled fields."""
    random_ca = entity.CustomAttribute()
    random_ca.ca_type = random.choice(AttributesTypes.ALL_TYPES)
    random_ca.title = cls._generate_title(random_ca.ca_type)
    random_ca.definition_type = random.choice(objects.all_objects)
    return random_ca

  @classmethod
  def _generate_title(cls, ca_type):
    """Generate title according to CustomAttribute type."""
    special_chars = string_utils.SPECIAL
    return append_random_string(
        "{}_{}_".format(ca_type, random_string(
            size=len(special_chars), chars=special_chars)))

  @classmethod
  def _fill_ca_entity_fields(cls, ca_object, **ca_object_fields):
    """Set the CustomAttributes object's attributes."""
    if ca_object_fields.get("ca_type"):
      ca_object.ca_type = ca_object_fields["ca_type"]
      ca_object.title = cls._generate_title(ca_object.ca_type)
    if ca_object_fields.get("definition_type"):
      ca_object.definition_type = ca_object_fields["definition_type"]
    if ca_object_fields.get("title"):
      ca_object.title = ca_object_fields["definition_type"]

    # "Placeholder" field exists only for Text and Rich Text.
    if (ca_object_fields.get("placeholder") and
        ca_object.ca_type in (AttributesTypes.TEXT,
                              AttributesTypes.RICH_TEXT)):
      ca_object.placeholder = ca_object_fields["placeholder"]

    if ca_object_fields.get("helptext"):
      ca_object.helptext = ca_object_fields["helptext"]
    if ca_object_fields.get("is_mandatory"):
      ca_object.is_mandatory = ca_object_fields["is_mandatory"]
    if ca_object_fields.get("ca_global"):
      ca_object.ca_global = ca_object_fields["ca_global"]

    # "Possible Values" - is a mandatory field for dropdown CustomAttribute.
    if ca_object.ca_type == AttributesTypes.DROPDOWN:
      if (ca_object_fields.get("multi_choice_options") and
              ca_object_fields["multi_choice_options"] is not None):
        ca_object.multi_choice_options =\
            ca_object_fields["multi_choice_options"]
      else:
        ca_object.multi_choice_options = random_list_of_strings(list_len=3)
    return ca_object

  @classmethod
  def _normalize_ca_definition_type(cls, ca_object):
    """Transform definition type to title form.

    Title from used for UI operations.
    For REST operations definition type should be interpreted as
    objects.get_singular().get_object_name_form().
    """
    ca_object.definition_type = objects.get_normal_form(
        ca_object.definition_type
    )
    return ca_object
