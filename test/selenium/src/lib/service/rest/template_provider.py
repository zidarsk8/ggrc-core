# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""The module provides functionality for working with JSON templates."""
# pylint: disable=too-few-public-methods
# pylint: disable=redefined-builtin
# pylint: disable=invalid-name

import copy
import json
import os

from lib.constants import objects, url


class TemplateProvider(object):
  """Provider of the methods for work with JSON templates."""
  _relationship = objects.get_singular(url.RELATIONSHIPS)
  _object_owner = objects.get_singular(url.OBJECT_OWNERS)
  _count = objects.COUNT
  _contact = objects.get_singular(url.CONTACTS)
  relative_path_template = "template/{0}.json"
  parsed_data = dict()

  @classmethod
  def generate_template_as_dict(cls, template, **kwargs):
    """Get template as dictionary from a predefined JSON file and attributes
    (items (kwargs): key=value).
    Return the dictionary like as {type: {key: value, ...}}.
    """
    path = os.path.join(os.path.dirname(__file__),
                        cls.relative_path_template.format(template))
    with open(path) as json_file:
      json_data = json_file.read()
    data = json.loads(json_data)
    cls.parsed_data[template] = data
    obj = copy.deepcopy(data)
    obj.update(kwargs)
    if template not in {cls._relationship, cls._object_owner, cls._count}:
      contact = ({cls._contact: cls.generate_object(1, objects.PEOPLE)})
      obj.update(contact)
    return {template: obj}

  @classmethod
  def update_template_as_dict(cls, template, **kwargs):
    """Update the template as the list of dictionary according to the
    attributes (items (kwargs): key=value).
    Return the list of dictionary like as [{type: {key: value, ...}}].
    """
    data = json.loads(template)
    type = data.iterkeys().next()
    value = data.itervalues().next()
    obj = copy.deepcopy(value)
    obj.update(kwargs)
    return {type: obj}

  @staticmethod
  def generate_object(obj_id, obj_type):
    """Return minimal object representation by id and type."""
    result = {}
    result["id"] = obj_id
    result["href"] = "/".join([url.API, obj_type, str(obj_id)])
    result["type"] = objects.get_singular(obj_type)
    return result
