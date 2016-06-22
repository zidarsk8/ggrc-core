# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

# pylint: disable=too-few-public-methods

"""The module provides API for creating and manipulating GGRC's business
objects via REST"""

import json

from lib.service.rest.client import RestClient
from lib.constants import url


class BaseService(object):
  """Base class for business layer's services objects"""
  def __init__(self):
    self.client = RestClient(self.ENDPOINT)

  @staticmethod
  def get_list_of_created_objects(response):
    """Forms the list of business entities from response"""
    def minimize(object_element):
      """Minimize response json data to request ready format"""
      obj = object_element[1].values()[0]
      return {"id": obj["id"], "href": obj["selfLink"], "type": obj["type"]}
    return [minimize(object_element=x) for x in json.loads(response.text)]


class ControlsService(BaseService):
  """Incapsulates logic for working with business entity Control"""
  ENDPOINT = url.CONTROLS

  def create_controls(self, count):
    return self.get_list_of_created_objects(
        self.client.create_objects("control", count=count))


class ProgramsService(BaseService):
  """Incapsulates logic for working with business entity Program"""
  ENDPOINT = url.PROGRAMS

  def create_programs(self, count):
    return self.get_list_of_created_objects(
        self.client.create_objects("program", count=count))


class AuditsService(BaseService):
  """Incapsulates logic for working with business entity Audit"""
  ENDPOINT = url.AUDITS

  def create_audits(self, count, program):
    return self.get_list_of_created_objects(
        self.client.create_objects("audit", count=count, program=program))


class AssessmentsService(BaseService):
  """Incapsulates logic for working with business entity Assessment"""
  ENDPOINT = url.ASSESSMENTS

  def create_assessments(self, count, obj, audit):
    return self.get_list_of_created_objects(
        self.client.create_objects("assessment", count=count, object=obj,
                                   audit=audit))
