# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Base locust task module."""

import collections
import random
import json

import locust

from performance import generator
from performance import models


class BaseTaskSet(locust.TaskSet):
  """Base locust task set with object generator helpers."""
  # pylint: disable=too-many-instance-attributes,too-many-public-methods

  GAE = False
  EXCLUDE_OWNER_MODELS = {
      "Assessment",
      "Audit",
      "Program",
  }

  def __init__(self, *args, **kwargs):
    super(BaseTaskSet, self).__init__(*args, **kwargs)

    self.headers = {
        "X-Requested-By": "GGRC",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip, deflate, br"
    }

    self.headers_text = {
        "X-Requested-By": "GGRC",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": ("text/html,application/xhtml+xml,application/xml;q=0.9,"
                   "image/webp,*/*;q=0.8"),

    }
    self.role = "Admin"

    # id, relationship object
    self.relationships = collections.defaultdict(dict)

    # object type, object slug
    self.objects = collections.defaultdict(list)
    # audit id, child type, snapshot slug
    self.snapshots = collections.defaultdict(
        lambda: collections.defaultdict(list))
    # object type, cad data
    self.cads = collections.defaultdict(list)
    # audit id, template object type, template data
    self.assessment_templates = collections.defaultdict(
        lambda: collections.defaultdict(list))
    # object type, acr data
    self.acr = collections.defaultdict(list)

    # role name, person slug
    self.user_roles = collections.defaultdict(list)

    # id, person data
    self.people = {
        1: {
            "company": None,
            "email": "user@example.com",
            "id": 1,
            "name": "Example User"
        }
    }
    self.user_roles["Administrator"].append(generator.slug("Person", 1))

  def on_start(self):
    """ on_start is called when a Locust start before any task is scheduled """
    self._log_in()
    self.set_up()

  def set_up(self):
    self.get_all_objects()

  def _put(self, response, obj):
    """Generate an object PUT request."""
    headers = {
        "If-Match": response.headers["Etag"],
        "If-Unmodified-Since": response.headers["Last-Modified"],
    }
    headers.update(self.headers)
    model = obj["type"]
    data = {models.TABLES_SINGULAR[model]: obj}
    response = self.client.put(
        obj["selfLink"],
        json=data,
        headers=headers,
        name="{} /api/{}/XYZ".format(self.role, models.TABLES_PLURAL[model]),
    )

  def update_object(self, slug, changes=None):
    """Fetch update and PUT an object."""
    response = self.get_from_slug(slug)
    obj = response.json().values()[0]
    if changes:
      obj.update(changes)
    else:
      obj = generator.update_properties(obj)
      obj = generator.update_acl(obj)
      if obj["type"] == "Assessment":
        obj = generator.update_cavs_new(obj, self.objects)
      else:
        obj = generator.update_cavs_old(obj, self.objects)
    self._put(response, obj)

  def get_multiple(self, model, ids):
    """Generate GET request with id__in filter."""
    model_plural = models.TABLES_PLURAL[model]
    response = self.client.get(
        "/api/{}".format(model_plural),
        params={"id__in": ",".join(str(id_) for id_ in ids)},
        headers=self.headers,
        name="{} id_in ({}) /api/{}".format(self.role, len(ids), model_plural),
    )
    return response

  def get_single(self, model, id_):
    """Generate single model GET request."""
    model_plural = models.TABLES_PLURAL[model]
    response = self.client.get(
        "/api/{}/{}".format(model_plural, id_),
        headers=self.headers,
        name="{} /api/{}/XYZ".format(self.role, model_plural),
    )
    return response

  def get_from_slug(self, slug):
    """Get a single object from a slug."""
    return self.get_single(slug["type"], slug["id"])

  def get_objects(self, model):
    """Get all objects of a single type."""
    model_plural = models.TABLES_PLURAL[model]
    model_collection = "{}_collection".format(model_plural)
    response = self.client.get(
        "/api/{}".format(model_plural),
        headers=self.headers,
        name="/_initial object get",
    )
    if response.status_code == 200:
      response_json = response.json()
      data = response_json[model_collection][model_plural]
      self._store_object(model, data)

  def get_all_objects(self):
    """Get all objects of all types."""
    response = self.client.get(
        "/search",
        params={
            "q": "",
            "types": ",".join(models.INITIAL_MODELS),
            "counts_only": True,
        },
        headers=self.headers,
        name="/_search model counts",
    )
    counts = response.json()["results"]["counts"]
    for model, count in counts.items():
      self.objects[model] = [
          generator.slug(model, i + 1)
          for i in range(count)
      ]
    for model in models.SPECIAL_INITIAL_MODELS:
      self.get_objects(model)

  def _get_object(self, slug):
    """Retrieve full object from slug."""
    obj = None
    if slug["type"] == "Relationship":
      obj = self.relationships.get(slug["id"])
    if slug["type"] == "Person":
      obj = self.people.get(slug["id"])
    if not obj:
      response = self.get_from_slug(slug)
      obj = response.json().values()[0]
      if obj["type"] == "Relationship":
        self.relationships[obj["id"]] = obj
      if obj["type"] == "Person":
        self.people[obj["id"]] = obj
    return obj

  def _log_in(self, person=None):
    """Log in as a given user."""
    if not person:
      person = {"name": "Example User", "email": "user@example.com"}
    else:
      obj = self.people.get(person["id"], self._get_object(person))
      person = {"name": obj["name"], "email": obj["email"]}

    if self.GAE:
      params = {"action": "Login"}
      params.update(person)
      self.client.get("/logout")
      self.client.get("/_ah/login", params=params, name="/_ah/login")
      self.client.get("/dashboard")
    else:
      headers = {"X-ggrc-user": json.dumps(person)}
      self.client.get("/logout")
      self.client.get("/login", headers=headers)

  def _store_cads(self, response_json):
    """Store custom attribute definitions to local variable."""
    for data in response_json:
      definition_model = models.TABLES_SINGULAR_REV[data["definition_type"]]
      self.cads[definition_model].append(data)

  def _store_assessment_templates(self, response_json):
    """Store assessment template to local variable."""
    for data in response_json:
      rel_slug = data["related_sources"] or data["related_destinations"]
      relationship = self._get_object(rel_slug[0])
      if relationship["source"]["type"] == "Audit":
        id_ = relationship["source"]["id"]
      elif relationship["destination"]["type"] == "Audit":
        id_ = relationship["destination"]["id"]
      else:
        raise Exception("Invalid template")
      obj = data["template_object_type"]
      self.assessment_templates[id_][obj].append(data)

  def _store_snapshots(self, response_json):
    """Store snapshots to local variable."""
    for data in response_json:
      audit_id = data["parent"]["id"]
      object_type = data["child_type"]
      self.snapshots[audit_id][object_type].append(generator.obj_to_slug(data))

  def _store_relationships(self, response_json):
    """Store relationships to local variable."""
    for data in response_json:
      self.relationships[data["id"]] = data

  def _store_user_roles(self, response_json):
    """Store user roles to local variable."""
    for data in response_json:
      role_name = models.ROLES[data["role"]["id"]]
      self.user_roles[role_name].append(data["person"])

  def _store_people(self, response_json):
    """Store people to local variable."""
    filter_keys = ["id", "name", "email", "company"]
    for data in response_json:
      self.people[data["id"]] = {key: data[key] for key in filter_keys}

  def _store_object(self, model, response_json, unpack=False):
    """Store objects received by a response in local objects field.

    Args:
      model: Model name.
      response_json: JSON of the request respose.
      unpack: boolean value that should be true if response is from a
        collection post request. Those responses have status codes included.
    """
    if unpack:
      response_json = [
          item[1][models.TABLES_SINGULAR[model]]
          for item in response_json
      ]

    if model == "CustomAttributeDefinition":
      self._store_cads(response_json)
    elif model == "AssessmentTemplate":
      self._store_assessment_templates(response_json)
    elif model == "Snapshot":
      self._store_snapshots(response_json)
    elif model == "Relationship":
      self._store_relationships(response_json)
    elif model == "Person":
      self._store_people(response_json)
    elif model == "UserRole":
      self._store_user_roles(response_json)

    new_slugs = [
        generator.obj_to_slug(item)
        for item in response_json
    ]

    self.objects[model].extend(new_slugs)

    return new_slugs

  def _post(self, model, data, name=None, as_prefix=True):
    """Send client post request and store the result locally."""
    url = "/api/{}".format(models.TABLES_PLURAL[model])
    if name and as_prefix:
      name = "{} {}".format(name, url)
    elif not name:
      name = url

    response = self.client.post(
        url,
        json=data,
        headers=self.headers,
        name="{} {}".format(self.role, name),
    )
    response_json = response.json()
    return self._store_object(model, response_json, unpack=True)

  def create_cads(self, types=None, prefixes=None):
    """Create custom attribute definitions for all models.

    This function creates types * prefixes CADs for each object.

    Args:
      types: list of CAD types that should be added.
      prefixes: prefix for cad title, prefix "2" will be set as mandatory
    """
    if not types:
      types = models.CAD_TYPES
    if not prefixes:
      prefixes = ["1", "2"]
    data = []
    for type_ in types:
      for model in models.CUSTOM_ATTRIBUTABLE:
        for prefix in prefixes:
          mandatory = prefix == "2"
          data.extend(generator.cad(model, type_, prefix, mandatory))
    self._post("CustomAttributeDefinition", data)

  def create_acr(self):
    pass

  def create_user_role(self, role_name, people_slugs, context=None):
    """Create user role entry for given people."""
    data = generator.user_role(role_name, people_slugs, context=context)
    count = len(people_slugs)
    name = "count {}".format(count) if count > 1 else ""
    return self._post("UserRole", data, name=name)

  def create_people(self, roles=None, count=25):
    """Create random people with the give roles."""
    if not roles:
      roles = [
          "Reader",
          "Editor",
          "Administrator",
          "Creator",
      ]
    slugs = []
    for role in roles:
      for i in range(count):
        data = generator.person(name="{} {}".format(role, i))
        people_slugs = self._post("Person", data)
        self.create_user_role(role, people_slugs)
        slugs.extend(people_slugs)
    return slugs

  def create_object_owners(self, object_slugs, **kwargs):
    """Create random object owner entries for given objects."""
    data = generator.object_owner(self.objects, object_slugs)
    self._post("ObjectOwner", data, **kwargs)

  def create_relationships(self, sources, destinations, batch_size=1000):
    """Create relationship entries."""
    if not sources or not destinations:
      return []
    slugs = []
    model = "Relationship"
    for source in sources:
      destination_chunks = [
          destinations[i: i + batch_size]
          for i in range(0, len(destinations), batch_size)
      ]
      for chunk in destination_chunks:
        name = "count={}".format(len(chunk))
        data = generator.relationship(source, chunk)
        slugs.extend(self._post(model, data, name=name))
    return slugs

  def create_programs_with_mappings(self, models_, mapping_count, count=1):
    """Create multiple program all mapped to multiple objects.

    Args:
      models_: list of models that will be mapped to the programs.
      mapping_count: number of objects of each model that will be mapped to a
        single program.
      count: number of programs created.
    Returns:
      list of newly created program slugs.
    """
    programs = self.create_programs(count=count)
    for model in models_:
      objects = generator.random_objects(model, mapping_count, self.objects)
      self.create_relationships(programs, objects)
    return programs

  def create_audits(self, programs=None, **kwargs):
    """Create audit entries from given programs."""
    audits = []
    get_snapshots = kwargs.pop("get_snapshots", True)
    count = kwargs.get("count", 1)
    kwargs["count"] = 1
    for program in programs:
      for _ in range(count):
        audit = self.create_object("Audit", program=program, **kwargs)
        people = generator.random_objects("Person", 2, self.objects)
        self.create_user_role("Auditor", people, audit[0]["context"])
        audits.append(audit)

    if get_snapshots:
      self.get_objects("Snapshot")
    return audits

  def create_at(self, audits, at_models=None, count=1, **kwargs):
    """Create assessment template entries for the given audit.

    This generates (len(audits) * len(at_models) * count) assessment templates.
    """
    if not at_models:
      at_models = [
          "Control",
          "Objective",
          "Facility",
      ]
    for audit in audits:
      if not audit.get("context"):
        audit = self._get_object(audit)
      for _ in range(count):
        for model in at_models:
          data = generator.assessment_template(
              audit=audit,
              template_object=model,
              prefixes=kwargs.get("prefixes")
          )
          self._post("AssessmentTemplate", data, kwargs.get("name"))

  def set_random_user(self, roles=None):
    """Login as a random user of a given role."""
    if not roles:
      roles = ["Administrator"]
    role = random.choice(roles)
    person = generator.random_object(role, self.user_roles)
    self.role = role[:5]
    self._log_in(person=person)
    return person

  def create_object(self, model, count=1, batch_size=1, **kwargs):
    """Create a generic object entry."""
    all_slugs = []
    random_user = kwargs.pop("random_user", False)

    while count > 0:
      if random_user:
        self.set_random_user(roles=["Administrator"])
      batch_count = min(count, batch_size)
      name = None if batch_count == 1 else "count={}".format(batch_count)
      count -= batch_count
      data = generator.generate(
          model=model,
          count=batch_count,
          objects=self.objects,
          cads=self.cads[model],
          acr=self.acr[model],
          **kwargs
      )
      slugs = self._post(model, data, name=name)
      all_slugs.extend(slugs)
      if model not in self.EXCLUDE_OWNER_MODELS:
        self.create_object_owners(
            slugs,
            name=name,
        )
    return all_slugs

  def create_facilities(self, **kwargs):
    return self.create_object("Facility", **kwargs)

  def create_controls(self, **kwargs):
    return self.create_object("Control", **kwargs)

  def create_markets(self, **kwargs):
    return self.create_object("Market", **kwargs)

  def create_regulations(self, **kwargs):
    return self.create_object("Regulation", **kwargs)

  def create_objectives(self, **kwargs):
    return self.create_object("Objective", **kwargs)

  def create_programs(self, **kwargs):
    """Create program entries.

    Since program manager is always the person who creates it, this function
    sets a different user for each request and sets the default user at the
    end.
    """
    response = self.create_object("Program", random_user=True, **kwargs)
    self._log_in()
    return response

  def create_org_groups(self, **kwargs):
    return self.create_object("OrgGroup", **kwargs)

  def autogenerate_assessments(self, audits, template_models, count):
    """Auto-generate assessments from templates."""
    model = "Assessment"
    all_slugs = []
    if not template_models:
      template_models = ["Control"]
    for audit in audits:
      if not audit["context"]:
        audit = self.get_from_slug(audit)
      for template_model in template_models:
        name = None if count == 1 else "count={}".format(count)
        audit_templates = self.assessment_templates[audit["id"]]
        template = generator.random_object(template_model, audit_templates)
        data = generator.assessment_from_template(
            audit=audit,
            template=template,
            snapshots=self.snapshots,
            count=count,
        )
        self.set_random_user(roles=["Administrator"])
        slugs = self._post(model, data, name=name)
        all_slugs.extend(slugs)
    self._log_in()
    return all_slugs
