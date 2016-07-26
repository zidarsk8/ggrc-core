# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

# pylint: disable=too-few-public-methods

"""The module contains functionality for working with json templates"""

import copy
import json
import os

from lib.constants import url
from lib.constants import objects


class TemplateProvider(object):
  """Processes json templates"""
  RELATIVE_PATH_TEMPLATE = "template/{0}.json"
  parsed_data = dict()

  @staticmethod
  def get_template_as_dict(obj_type, **kwargs):
    """Return object representation based on json template"""
    try:
      obj = copy.deepcopy(TemplateProvider.parsed_data[obj_type])
    except KeyError:
      path = os.path.join(
          os.path.dirname(__file__),
          TemplateProvider.RELATIVE_PATH_TEMPLATE.format(obj_type))
      with open(path) as json_file:
        json_data = json_file.read()
      data = json.loads(json_data)
      TemplateProvider.parsed_data[obj_type] = data
      obj = copy.deepcopy(data)
    obj.update(kwargs)
    contact = {"contact": TemplateProvider.generate_object(1, objects.PEOPLE)}
    obj.update(contact)
    return {obj_type: obj}

  @staticmethod
  def generate_object(obj_id, obj_type):
    """Return minimal object representation by id and type"""
    result = {}
    result["id"] = obj_id
    result["href"] = "/".join([url.API, obj_type, str(obj_id)])
    result["type"] = objects.get_singular(obj_type)
    return result
