# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""The module provides services for creating and manipulating GGRC's business
objects via REST API."""
# pylint: disable=too-few-public-methods

import json

import re

from lib import environment
from lib.constants import url, objects
from lib.entities.entities_factory import (
    ProgramFactory, AuditFactory, AsmtTmplFactory, AsmtFactory, ControlFactory,
    PersonFactory)
from lib.service.rest.client import RestClient


class BaseService(object):
  """Base class for business layer's services objects."""

  def __init__(self):
    self.client = RestClient(self.ENDPOINT)
    self._relationship = objects.get_singular(url.RELATIONSHIPS)
    self._object_owner = objects.get_singular(url.OBJECT_OWNERS)
    self._count = objects.COUNT

  def create_objs(self, count, factory, **kwargs):
    """Create business objects used entities factories and REST API
    (responses from web-server parsed to list of attributes (list of dicts))
    Return list of created objects.
    """
    list_objs = [factory.create() for _ in xrange(count)]
    list_attrs = [
        self.get_obj_attrs(self.client.create_object(
            type=obj.type, title=obj.title, slug=obj.code, **kwargs)) for
        obj in list_objs]
    return [self.set_obj_attrs(attrs, obj, **kwargs) for
            attrs, obj in zip(list_attrs, list_objs)]

  @staticmethod
  def get_obj_attrs(response):
    """Form the dictionary of business object's attributes (dict's items)
    from server response.
    """
    def get_items_from_obj_el(obj_el):
      """Get values from dict object element (obj_el) and create new dict of
      items.
      """
      return {"id": obj_el.get("id"), "href": obj_el.get("selfLink"),
              "type": obj_el.get("type"), "title": obj_el.get("title"),
              "code": obj_el.get("slug"),
              "url": environment.APP_URL + obj_el.get("viewLink")[1:],
              "name": re.search(r"\/([a-z_]*)\/",
                                obj_el.get("viewLink")).group(1),
              "last_update": obj_el.get("updated_at")}
    resp = json.loads(response.text)
    if isinstance(resp, list) and len(resp[0]) == 2:
      return get_items_from_obj_el(resp[0][1].itervalues().next())
    elif isinstance(resp, dict) and len(resp) == 1:
      return get_items_from_obj_el(resp.itervalues().next())
    else:
      pass

  @staticmethod
  def set_obj_attrs(attrs, obj, **kwargs):
    """Update business object's attributes according type of object and
    list of dicts with business object's attributes (dict's items).
    """
    if attrs.get("id"):
      obj.id = attrs["id"]
    if attrs.get("href"):
      obj.href = attrs["href"]
    if attrs.get("last_update"):
      obj.last_update = attrs["last_update"]
    if attrs.get("code") == obj.code:
      obj.code = attrs["code"]
    if attrs.get("title") == obj.title:
      obj.title = attrs["title"]
    if kwargs:
      # for Audit objects
      if kwargs.get("program") and kwargs.get("program").get("title"):
        obj.program = kwargs["program"]["title"]
      # for Assessment Template objects
      if kwargs.get("audit") and kwargs.get("audit").get("title"):
        obj.audit = kwargs["audit"]["title"]
      # for Assessment objects
      if kwargs.get("object") and kwargs.get("object").get("title"):
        obj.object = kwargs["object"]["title"]
    return obj

  def update_objs(self, list_old_objs, factory):
    """Update business objects used old objects (list_old_objs) as target,
    entities factories as new attributes data generator,
    REST API as service for provide that.
    Return list of updated objects.
    """
    list_new_objs = [factory.create() for _ in xrange(len(list_old_objs))]
    list_new_attrs = [
        self.get_obj_attrs(self.client.update_object(
            href=old_obj.href, title=new_obj.title,
            slug=new_obj.code)) for
        old_obj, new_obj in zip(list_old_objs, list_new_objs)]
    return [self.set_obj_attrs(new_attrs, new_obj) for
            new_attrs, new_obj in zip(list_new_attrs, list_new_objs)]


class ControlsService(BaseService):
  """Encapsulates logic for working with business entity Control."""
  ENDPOINT = url.CONTROLS

  def create(self, count):
    return self.create_objs(count=count, factory=ControlFactory())

  def update(self, objs):
    return self.update_objs(list_old_objs=[objs], factory=ControlFactory())


class ProgramsService(BaseService):
  """Encapsulates logic for working with business entity Program."""
  ENDPOINT = url.PROGRAMS

  def create(self, count):
    return self.create_objs(count=count, factory=ProgramFactory())


class AuditsService(BaseService):
  """Encapsulates logic for working with business entity Audit."""
  ENDPOINT = url.AUDITS

  def create(self, count, program):
    return self.create_objs(count=count, factory=AuditFactory(),
                            program=program.__dict__)


class AsmtTmplsService(BaseService):
  """Encapsulates logic for working with business entity
  Assessment Template.
  """
  ENDPOINT = url.ASSESSMENT_TEMPLATES

  def create(self, count, audit):
    return self.create_objs(count=count, factory=AsmtTmplFactory(),
                            audit=audit.__dict__)


class AssessmentsService(BaseService):
  """Encapsulates logic for working with business entity Assessment."""
  ENDPOINT = url.ASSESSMENTS

  def create(self, count, obj, audit):
    return self.create_objs(count=count, factory=AsmtFactory(),
                            object=obj.__dict__, audit=audit.__dict__)


class RelationshipsService(BaseService):
  """Encapsulates logic for create relationships between business objects."""
  ENDPOINT = url.RELATIONSHIPS

  def create(self, src_obj, dest_objs):
    if isinstance(dest_objs, list):
      return [
          self.client.create_object(
              type=self._relationship, source=src_obj.__dict__,
              destination=dest_obj.__dict__) for dest_obj in dest_objs]
    else:
      return self.client.create_object(
          type=self._relationship, source=src_obj.__dict__,
          destination=dest_objs.__dict__)


class ObjectsOwnersService(BaseService):
  """Encapsulates logic for assign owners to the business objects."""
  ENDPOINT = url.OBJECT_OWNERS

  def create(self, objs, owner=PersonFactory().default()):
    if isinstance(objs, list):
      return [
          self.client.create_object(
              type=self._object_owner, ownable=obj.__dict__,
              person=owner.__dict__) for obj in objs]
    else:
      return self.client.create_object(
          type=self._object_owner, ownable=objs.__dict__,
          person=owner.__dict__)


class ObjectsInfoService(BaseService):
  """Encapsulates logic for get information about the business objects."""
  ENDPOINT = url.QUERY

  def total_count(self, obj_name):
    """Get total count of existing objects in app according the object name."""
    resp = self.client.create_object(type=self._count, object_name=obj_name)
    dict_resp = json.loads(resp.text)[0]
    return dict_resp.get(obj_name).get("total")
