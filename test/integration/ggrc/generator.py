# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

import names
import random
import string
import datetime

from ggrc import db
from ggrc import models
from ggrc.app import app
from ggrc.services import common
from ggrc_basic_permissions.models import UserRole, Role
from integration.ggrc import api_helper


class Generator():
  """Generator base class."""

  def __init__(self):
    self.api = api_helper.Api()
    self.resource = common.Resource()

  def random_str(self, length=8,
                 chars=string.ascii_uppercase + string.digits + "  _.-"):
    return ''.join(random.choice(chars) for _ in range(length))

  def random_date(self, start=datetime.date.today(), end=None):
    if not end or start > end:
      end = start + datetime.timedelta(days=7)
    return start + datetime.timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())))

  def get_object(self, obj_class, obj_id):
    try:
      return db.session.query(obj_class).filter(obj_class.id == obj_id).one()
    except:
      return None

  def generate(self, obj_class, obj_name=None, data=None):
    if obj_name is None:
      obj_name = obj_class._inflector.table_plural
    if data is None:
      data = {}
    response = self.api.post(obj_class, data)
    response_obj = None
    if response.json:
      response_obj = self.get_object(obj_class, response.json[obj_name]['id'])
    return response, response_obj

  def modify(self, obj, obj_name, data):
    obj_class = obj.__class__
    response = self.api.put(obj, data)
    response_obj = None
    if response.json:
      response_obj = self.get_object(obj_class, response.json[obj_name]['id'])
    return response, response_obj

  def obj_to_dict(self, obj, model_name=None):
    with app.app_context():
      return self.resource.object_for_json(obj, model_name)


class ObjectGenerator(Generator):

  def create_stub(self, obj):
    return {
        "id": obj.id,
        "href": "/api/{}/{}".format(obj._inflector.table_name, obj.id),
        "type": obj.type,
    }

  def generate_object(self, obj_class, data=None):
    if data is None:
      data = {}
    obj_name = obj_class._inflector.table_singular
    obj = obj_class(title=self.random_str())
    obj_dict = self.obj_to_dict(obj, obj_name)
    obj_dict[obj_name].update({"owners": [{
        "id": 1,
        "href": "/api/people/1",
        "type": "Person"
    }]})
    obj_dict[obj_name].update(data)
    return self.generate(obj_class, obj_name, obj_dict)

  def generate_user_role(self, person, role):
    data = {
        "user_role": {
            "context": None,
            "person": self.create_stub(person),
            "role": self.create_stub(role),
        }
    }
    return self.generate(UserRole, "user_role", data)

  def generate_person(self, data={}, user_role=None):
    obj_name = 'person'
    name = names.get_full_name()
    default = {
        obj_name: {
            "context": None,
            "name": name,
            "email": "%s@test.com" % name.replace(" ", ".").lower(),
        }
    }
    default[obj_name].update(data)
    response, person = self.generate(models.Person, obj_name, default)

    if person and user_role:
      role = db.session.query(Role).filter(Role.name == user_role).first()
      self.generate_user_role(person, role)

    return response, person

  def generate_random_objects(self, count=5):
    random_objects = []
    classes = [
        models.Control,
        models.Objective,
        models.Standard,
        models.System,
        models.OrgGroup,
    ]
    for _ in range(count):
      obj_class = random.choice(classes)
      response, obj = self.generate_object(obj_class)
      random_objects.append(obj)
    return random_objects

  def generate_random_people(self, count=5, **kwargs):
    random_people = []
    for _ in range(count):
      _, person = self.generate_person(**kwargs)
      if person:
        random_people.append(person)
    return random_people

  def generate_notification_setting(self, user_id, notif_type, enable_flag):
    obj_name = "notification_config"
    data = {
        obj_name: {
            "person_id": user_id,
            "notif_type": notif_type,
            "enable_flag": enable_flag,
            "context": None,
            "type": "NotificationConfig",
        }
    }
    return self.generate(models.NotificationConfig, obj_name, data)

  def generate_custom_attribute(self, definition_type, **kwargs):
    obj_name = "custom_attribute_definition"
    data = {
        obj_name: {
            "title": kwargs.get("title", self.random_str()),
            "custom_attribute_definitions": [],
            "custom_attributes": {},
            "definition_type": definition_type,
            "modal_title": kwargs.get("modal_title", self.random_str()),
            "attribute_type": kwargs.get("attribute_type", "Text"),
            "mandatory": kwargs.get("mandatory", False),
            "helptext": kwargs.get("helptext", False),
            "placeholder": kwargs.get("placeholder", False),
            "context": {"id": None},
            "multi_choice_options": kwargs.get("options", False),
        }
    }
    data[obj_name].update(kwargs)
    self.generate(models.CustomAttributeDefinition, obj_name, data)
