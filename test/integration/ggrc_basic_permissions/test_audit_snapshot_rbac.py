# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test audit RBAC"""

from os.path import abspath
from os.path import dirname
from os.path import join
from collections import defaultdict
from integration.ggrc.converters import TestCase
from integration.ggrc.api_helper import Api

import integration.ggrc.generator

from ggrc import db
from ggrc.models import all_models


class TestAuditRBAC(TestCase):
  """Test audit RBAC"""

  CSV_DIR = join(abspath(dirname(__file__)), "test_csvs")

  def setUp(self):
    """Imports test_csvs/audit_rbac_snapshot_create.csv needed by the tests"""
    TestCase.setUp(self)
    self.api = Api()
    self.objgen = integration.ggrc.generator.ObjectGenerator()
    self.client.get("/login")
    filename = "audit_rbac_snapshot_create.csv"
    self.import_file(filename)
    self.people = all_models.Person.eager_query().all()

    self.program = db.session.query(all_models.Program).filter(
        all_models.Program.slug == "PMRBACPROGRAM-1"
    ).one()

    sources = set(r.source for r in self.program.related_sources)
    destinations = set(r.destination
                       for r in self.program.related_destinations)
    related = [obj for obj in sources.union(destinations)
               if not isinstance(obj, all_models.Person)]
    self.related_objects = related

    self.audit = self.create_audit()

    self.snapshots = all_models.Snapshot.eager_query().all()

    self.sanity_check()

  def create_audit(self):
    """Create default audit for audit snapshot RBAC tests"""
    _, audit = self.objgen.generate_object(all_models.Audit, {
        "title": "Snapshotable audit",
        "program": {"id": self.program.id},
        "status": "Planned",
        "snapshots": {
            "operation": "create",
        },
        "context": {
            "type": "Context",
            "id": self.program.context_id,
            "href": "/api/contexts/{}".format(self.program.context_id)
        }
    })
    return audit

  def update_audit(self):
    """Update default audit"""
    self._import_file("audit_rbac_snapshot_update.csv")

    audit = all_models.Audit.query.filter(
        all_models.Audit.title == "Snapshotable audit"
    ).one()
    self.audit = audit

    self.api.modify_object(self.audit, {
        "snapshots": {
            "operation": "upsert"
        }
    })

  def sanity_check(self):
    """Sanity check if the audit_rbac.csv was imported correctly"""
    assert len(self.people) == 17, \
        "Expecting 17 people not {}.".format(len(self.people))
    assert len(self.related_objects) == 19, \
        "Expecting 19 objects mapped to program not {}.".format(
            len(self.related_objects))
    assert len(self.snapshots) == 19, \
        "Expecting 19 snapshots for default audit not {}.".format(
            len(self.snapshots))
    assert all(ss.parent_id == self.audit.id for ss in self.snapshots), \
        "All snapshots should be in default audit scope!"

  def read(self, objects):
    """Attempt to do a GET request for every object in the objects list"""
    responses = []
    for obj in objects:
      status_code = self.api.get(obj.__class__, obj.id).status_code
      responses.append((obj.type, status_code))
    return responses

  def update(self, objects):
    """Attempt to do a PUT request for every object in the objects list"""
    responses = []
    for obj in objects:
      response = self.api.get(obj.__class__, obj.id)
      status_code = response.status_code
      if response.status_code == 200:
        data = response.json
        data.update({
            "update_revision": "latest"
        })
        status_code = self.api.put(obj, data).status_code
      responses.append((obj.type, status_code))
    return responses

  def call_api(self, method, expected_statuses):
    """Calls the REST api with a given method and returns a list of
       status_codes that do not match the expected_statuses dict"""
    all_errors = []
    for person in self.people:
      self.api.set_user(person)
      responses = method(self.snapshots + [self.audit])
      for type_, code in responses:
        if code != expected_statuses[person.email]:
          all_errors.append("{} does not have {} access to {} ({})".format(
              person.email, method.__name__, type_, code))
    return all_errors

  def test_read_access_on_mapped(self):
    """Test READ access to snapshotted objects of default audit"""
    expected_statuses = defaultdict(lambda: 200)
    for exception in ("creator@test.com",):
      expected_statuses[exception] = 403
    errors = self.call_api(self.read, expected_statuses)
    assert not errors, "\n".join(errors)

  def test_update_access_on_mapped(self):
    """Test UPDATE access to snapshotted objects of default audit"""
    self.update_audit()

    expected_statuses = defaultdict(lambda: 200)
    for exception in ("creator@test.com", "reader@test.com",
                      "creatorpr@test.com", "readerpr@test.com"):
      expected_statuses[exception] = 403
    errors = self.call_api(self.update, expected_statuses)
    assert not errors, "\n".join(errors)
