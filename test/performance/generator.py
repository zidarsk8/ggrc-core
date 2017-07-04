# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Helper module for generating valid model data from model templates."""

import random
import string

from performance import models
from performance import templates

CAD_MULTICHOICE_OPTIONS = ["one", "two", "three", "four", "five"]


def random_str(length=8, prefix="", chars=None):
  """Generate a random string."""
  chars = chars or string.ascii_uppercase + string.digits + "  _.-"
  return prefix + "".join(random.choice(chars) for _ in range(length))


def random_object(model, objects):
  """Select a random object of a given model."""
  if objects[model]:
    return random.choice(objects[model])
  return {}


def random_objects(model, count, objects):
  """Select up to count random non repeating objects."""
  model_objects = objects[model]
  indexes = range(len(model_objects))
  random.shuffle(indexes)
  return [model_objects[i] for i in indexes[:count]]


def obj_to_slug(obj):
  """Generate object slug from full object data."""
  return {
      "id": obj["id"],
      "href": obj["selfLink"],
      "type": obj["type"],
      "context": obj["context"],
  }


def slug(model, id_):
  """Generate object slug from model and id."""
  return {
      "id": id_,
      "href": "/api/{}/{}".format(models.TABLES_PLURAL[model], id_),
      "type": model,
  }


def person(count=1, name=None):
  """Generate random Person data."""
  content = []
  for _ in range(count):
    data = templates.get_template("Person")
    name = name or random_str(chars=string.ascii_lowercase)
    data["name"] = name
    data["email"] = name.replace(" ", ".") + "@example.com"
    content.append({"person": data})
  return content


def user_role(role_name, people_slugs, context=None):
  """Generate user role data for the given role name."""
  content = []
  role_id = models.ROLES_REV[role_name]
  for person_slug in people_slugs:
    data = templates.get_template("UserRole")
    data["role"] = slug("Role", role_id)
    data["person"] = person_slug
    data["context"] = context
    content.append({"user_role": data})
  return content


def cad(model, type_, prefix="", mandatory=False):
  """Generate custom attribute definition data."""
  options = ""
  if type_ == "Dropdown":
    options = ",".join(CAD_MULTICHOICE_OPTIONS)
  data = templates.get_template("CustomAttributeDefinition")
  data["title"] = "{} {} {}".format(
      prefix, models.TITLES_SINGULAR[model], type_)
  data["attribute_type"] = type_
  data["definition_type"] = models.TABLES_SINGULAR[model]
  data["mandatory"] = mandatory
  data["multi_choice_options"] = options
  content = [{"custom_attribute_definition": data}]
  return content


def object_owner(objects, object_slugs):
  """Generate object owner data."""
  people = objects["Person"]
  content = []
  for object_slug in object_slugs:
    data = templates.get_template("ObjectOwner")
    data["person"] = random.choice(people)
    data["ownable"] = object_slug
    content.append({"object_owner": data})
  return content


def get_cav_value(cad_, objects):
  """Get a single random value for the given custom attribute."""
  def cad_multichoice():
    """Get a random cad multi-choice option."""
    options = cad_["multi_choice_options"].split(",")
    if not cad_["mandatory"]:
      options.append("")
    return random.choice(options)

  people = objects["Person"]
  value_map = {
      "Map:Person": lambda: "Person:{}".format(random.choice(people)["id"]),
      "Dropdown": cad_multichoice,
      "Checkbox": lambda: random.choice([True, False]) or cad_["mandatory"],
      "Date": lambda: "2017-06-21",
      "Rich Text": lambda: random_str(length=random.randint(50, 200)),
      "Text": lambda: random_str(length=random.randint(10, 50)),
  }
  return value_map[cad_["attribute_type"]]()


def cavs_old(cads, objects):
  """Generate values for obsolete custom attribute values API."""
  return {
      str(cad_["id"]): get_cav_value(cad_, objects)
      for cad_ in cads
  }


def acl(acrs, objects, count=2, random_count=False):
  """Generate access control list data."""
  content = []
  for acr in acrs:
    count_ = random.randint(0, count) if random_count else count
    for _ in range(count_):
      content.append({
          "ac_role_id": acr["id"],
          "person": random_object("Person", objects),
      })
  return content


def relationship(source, destinations):
  """Generate relationships data."""
  content = []
  model = "Relationship"
  for destination in destinations:
    data = templates.get_template(model)
    pair = [source, destination]
    random.shuffle(pair)
    data["source"] = pair[0]
    data["destination"] = pair[1]
    content.append({models.TABLES_SINGULAR[model]: data})
  return content


def generate(model, count, objects, cads, acr, **kwargs):
  """Generate a generic model.

  Args:
    model: model name that we wish to generate.
    count: amount of models.
    objects: dict of lists containg different objects stubs under model name
      key.
    cads: list of custom attribute definitions for the given model.
    acr: list of access control roles for the given model.
  """
  content = []
  value_map = {
      "title": lambda i: random_str(prefix="{} title ({}) ".format(model, i)),
      "description": lambda _: random_str(length=random.randint(50, 200)),
      "custom_attribute_definitions": lambda _: cads,
      "custom_attributes": lambda _: cavs_old(cads, objects),
      "access_control_list": lambda _: acl(acr, objects),
      "audit_firm": lambda _: random_object("OrgGroup", objects),
      "contact": lambda _: random.choice(objects["Person"]),
      "program": lambda _: kwargs.get("program",
                                      random_object("Program", objects))
  }
  model_count = len(objects[model])
  for i in range(count):
    data = templates.get_template(model)
    for key in data:
      if key in value_map:
        data[key] = value_map[key](model_count + i)
    content.append({models.TABLES_SINGULAR[model]: data})
  return content


def assessment_template(audit, template_object, prefixes=None):
  """Generate assessment template data."""
  model = "AssessmentTemplate"

  if not prefixes:
    prefixes = ["1", "2"]

  cad_properties = [
      "title",
      "attribute_type",
      "multi_choice_options",
      "attribute_name",  # this is an invalid property
      "multi_choice_mandatory",
      "mandatory",
  ]

  template_cads = []
  for type_ in models.CAD_TYPES:
    for prefix in prefixes:
      mandatory = prefix == "2"
      cad_data = cad(model, type_, prefix, mandatory)[0].values()[0]
      template_cad = {key: cad_data.get(key, "") for key in cad_properties}
      template_cads.append(template_cad)
  data = templates.get_template(model)
  data["title"] = "{} for {} - {}".format(model, template_object, random_str())
  data["custom_attribute_definitions"] = template_cads
  data["audit"] = audit
  data["context"] = audit["context"]
  data["template_object_type"] = template_object

  return [{models.TABLES_SINGULAR[model]: data}]


def assessment_from_template(audit, template, snapshots, count=10):
  """Generate assessments from an assessment template."""
  model = "Assessment"
  content = []
  template_object_type = template["template_object_type"]
  template_objects = random_objects(template_object_type, count, snapshots)
  for template_object in template_objects:
    data = templates.get_template("AssessmentGeneration")
    data["object"] = template_object
    data["audit"] = audit
    data["context"] = audit["context"]
    data["template"] = obj_to_slug(template)
    data["title"] = "Generated Assessment for Audit {}".format(audit["id"])
    content.append({models.TABLES_SINGULAR[model]: data})

  return content


def update_properties(obj):
  """Update first class properties of an object."""
  conclusions = ["", "Needs improvement", "Effective", "Ineffective"]
  value_map = {
      "description": lambda: random_str(length=random.randint(50, 200)),
      "notes": lambda: random_str(length=random.randint(50, 200)),
      "design": lambda: random.choice(conclusions),
      "operationally": lambda: random.choice(conclusions),
  }
  for key in obj:
    if key in value_map:
      obj[key] = value_map[key]()
  return obj


def update_cavs_new(obj, objects):
  """Update custom attribute values of an object with the new API."""
  cav_map = {
      cav["custom_attribute_id"]: cav
      for cav in obj["custom_attribute_values"]
  }

  new_cavs = []
  for cad_ in obj["custom_attribute_definitions"]:
    template = templates.get_template("CustomAttributeValue")
    cav = cav_map.get(cad_["id"], template)
    cav["attribute_value"] = get_cav_value(cad_, objects)
    cav["custom_attribute_id"] = cad_["id"]
    new_cavs.append(cav)

  obj["custom_attribute_values"] = new_cavs
  return obj


def update_cavs_old(obj, objects):
  """Update custom attribute values of an object with the old API."""
  cads = obj["custom_attribute_definitions"]
  obj["custom_attributes"] = cavs_old(cads, objects)
  return obj


def update_acl(obj):
  """Update access control list items of an object."""
  return obj
