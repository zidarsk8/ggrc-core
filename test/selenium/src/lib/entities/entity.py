# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Module for business entities"""


class CustomAttribute(object):
  """Class that represent model for Custom Attribute."""

  # pylint: disable=too-few-public-methods
  # pylint: disable=too-many-arguments
  # pylint: disable=too-many-instance-attributes
  __hash__ = None

  def __init__(self, obj_id=None, title=None,
               ca_type=None, definition_type=None,
               helptext="", placeholder=None,
               multi_choice_options=None,
               is_mandatory=False, ca_global=True):
    super(CustomAttribute, self).__init__()
    self.obj_id = obj_id
    self.title = title
    self.ca_type = ca_type
    self.definition_type = definition_type
    self.helptext = helptext
    self.placeholder = placeholder
    self.multi_choice_options = multi_choice_options
    self.is_mandatory = is_mandatory
    self.ca_global = ca_global

  def __repr__(self):
    return "{def_type}:{ca_type} {title};Mandatory:{mandatory}".format(
        ca_type=self.ca_type,
        title=self.title,
        mandatory=self.is_mandatory,
        def_type=self.definition_type)

  def __eq__(self, other):
    return (isinstance(other, self.__class__) and
            self.title == other.title and
            self.ca_type == other.ca_type and
            self.is_mandatory == other.is_mandatory and
            self.definition_type == other.definition_type)
